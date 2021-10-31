from django.conf import settings
from django.utils.translation import gettext_lazy as _


ASSIGNMENT_ANY = 0
ASSIGNMENT_MATCH_USERNAME = 1
# ASSIGNMENT_EXCEPT = 2 -- Deprecated upon addition of groups and flag matching as logic becomes painful to reason about
ASSIGNMENT_MATCH_GROUP = 3
ASSIGNMENT_STAFF = 4
ASSIGNMENT_SUPERUSER = 5

ASSIGNMENT_CHOICES = (
    (ASSIGNMENT_ANY, _("any")),
    (ASSIGNMENT_MATCH_USERNAME, _("username matches")),
    (ASSIGNMENT_MATCH_GROUP, _("has group")),
    (ASSIGNMENT_STAFF, _("is staff")),
    (ASSIGNMENT_SUPERUSER, _("is superuser")),
)

DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON = getattr(
    settings, "DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON", True
)

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = getattr(
    settings, "DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID", None
)
DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = getattr(
    settings, "DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET", None
)
DJANGO_ADMIN_SSO_OAUTH_SCOPE = getattr(
    settings, "DJANGO_ADMIN_SSO_OAUTH_SCOPE", "email"
)

DJANGO_ADMIN_SSO_AUTH_URI = getattr(
    settings, "DJANGO_ADMIN_SSO_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"
)
DJANGO_ADMIN_SSO_TOKEN_URI = getattr(
    settings, "DJANGO_ADMIN_SSO_TOKEN_URI", "https://accounts.google.com/o/oauth2/token"
)
DJANGO_ADMIN_SSO_PROFILE_API = getattr(
    settings, "DJANGO_ADMIN_SSO_PROFILE_API", ""
)
DJANGO_ADMIN_SSO_ROLES_API = getattr(
    settings, "DJANGO_ADMIN_SSO_ROLES_API", ""
)
DJANGO_ADMIN_SSO_REVOKE_URI = getattr(
    settings,
    "DJANGO_ADMIN_SSO_REVOKE_URI",
    "https://accounts.google.com/o/oauth2/revoke",
)
