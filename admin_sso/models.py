from __future__ import unicode_literals

import fnmatch

from django.db import models
from django.utils.translation import gettext_lazy as _

from admin_sso import settings


class AssignmentManager(models.Manager):
    def for_user_profile(self, username, roles, staff, superuser):
        def _match_groups(asm):
            for i in roles:
                if fnmatch.fnmatch(i, asm.match):
                    print(i, asm.match)
                    return True
            return False

        possible_assignments = self.all()
        used_assignment = None
        for assignment in possible_assignments:
            if assignment.match_mode == settings.ASSIGNMENT_ANY:
                used_assignment = assignment
                break
            elif assignment.match_mode == settings.ASSIGNMENT_MATCH_USERNAME:
                if fnmatch.fnmatch(username, assignment.match):
                    used_assignment = assignment
                    break
            elif assignment.match_mode == settings.ASSIGNMENT_MATCH_GROUP:
                if _match_groups(assignment):
                    used_assignment = assignment
                    break
            elif assignment.match_mode == settings.ASSIGNMENT_STAFF:
                if staff:
                    used_assignment = assignment
                    break
            elif assignment.match_mode == settings.ASSIGNMENT_SUPERUSER:
                if superuser:
                    used_assignment = assignment
                    break
        print(used_assignment)
        if used_assignment is None:
            return None
        return used_assignment


class Assignment(models.Model):
    match_mode = models.IntegerField(choices=settings.ASSIGNMENT_CHOICES)
    match = models.CharField(verbose_name="Match Pattern", max_length=255, blank=True)
    weight = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-weight",)
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments")

    def __str__(self):
        return "%s(%s)" % (
            dict(settings.ASSIGNMENT_CHOICES)[self.match_mode],
            self.match,
        )

    objects = AssignmentManager()
