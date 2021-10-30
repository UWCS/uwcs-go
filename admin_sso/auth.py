from django.contrib.auth import get_user_model

from admin_sso.models import Assignment


class DjangoSSOAuthBackend(object):
    def get_user(self, user_id):
        cls = get_user_model()
        try:
            return cls.objects.get(pk=user_id)
        except cls.DoesNotExist:
            return None

    def authenticate(self, request=None, **kwargs):
        username = kwargs.pop("username", None)
        roles = kwargs.pop("roles", set())
        staff = kwargs.pop("staff", False)
        superuser = kwargs.pop("superuser", False)

        assignment = Assignment.objects.for_user_profile(username, roles, staff, superuser)
        if assignment is None:
            return None

        return assignment.user
