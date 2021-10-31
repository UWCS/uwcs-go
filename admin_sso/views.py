import requests
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError

from admin_sso import settings

flow_kwargs = {
    "client_id": settings.DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID,
    "client_secret": settings.DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET,
    "scope": settings.DJANGO_ADMIN_SSO_OAUTH_SCOPE,
}
if settings.DJANGO_ADMIN_SSO_AUTH_URI:
    flow_kwargs["auth_uri"] = settings.DJANGO_ADMIN_SSO_AUTH_URI

if settings.DJANGO_ADMIN_SSO_TOKEN_URI:
    flow_kwargs["token_uri"] = settings.DJANGO_ADMIN_SSO_TOKEN_URI

if settings.DJANGO_ADMIN_SSO_REVOKE_URI:
    flow_kwargs["revoke_uri"] = settings.DJANGO_ADMIN_SSO_REVOKE_URI

flow_override = None


def start(request):
    flow = OAuth2WebServerFlow(
        redirect_uri=request.build_absolute_uri(
            reverse("admin:admin_sso_assignment_end")
        ),
        **flow_kwargs
    )

    return HttpResponseRedirect(flow.step1_get_authorize_url())


def end(request):
    if flow_override is None:
        flow = OAuth2WebServerFlow(
            redirect_uri=request.build_absolute_uri(
                reverse("admin:admin_sso_assignment_end")
            ),
            **flow_kwargs
        )
    else:
        flow = flow_override

    code = request.GET.get("code", None)
    if not code:
        return HttpResponseRedirect(reverse("admin:index"))
    try:
        credentials = flow.step2_exchange(code)
    except FlowExchangeError:
        return HttpResponseRedirect(reverse("admin:index"))
    print(credentials.__dict__)

    if credentials.access_token:
        user_data, user_groups = _complete_login(credentials.access_token)
        user_id = user_data["user"]["username"]
        roles = {i["name"] for i in user_groups["user"]["groups"]}
        should_superuser = user_groups["user"]["is_superuser"]
        should_staff = user_groups["user"]["is_staff"]
        user = authenticate(username=user_id, roles=roles, superuser=should_superuser, staff=should_staff)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse("admin:index"))

    # if anything fails redirect to admin:index
    return HttpResponseRedirect(reverse("admin:index"))


def _complete_login(access_token, **kwargs):
    profile_url = settings.DJANGO_ADMIN_SSO_PROFILE_API
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token),
        'Content-Type': 'application/json',
    }
    extra_data = requests.get(profile_url, headers=headers).json()
    profile_url = settings.DJANGO_ADMIN_SSO_ROLES_API
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token),
        'Content-Type': 'application/json',
    }
    extra_data_plus = requests.get(profile_url, headers=headers).json()
    return extra_data, extra_data_plus
