from __future__ import unicode_literals

import fnmatch

from django.db import models
from django.utils.translation import gettext_lazy as _

from admin_sso import settings


class AssignmentManager(models.Manager):
    def for_username(self, username):
        possible_assignments = self.all()
        used_assignment = None
        for assignment in possible_assignments:
            if assignment.username_mode == settings.ASSIGNMENT_ANY:
                used_assignment = assignment
                break
            elif assignment.username_mode == settings.ASSIGNMENT_MATCH:
                if fnmatch.fnmatch(username, assignment.username):
                    used_assignment = assignment
                    break
            elif assignment.username_mode == settings.ASSIGNMENT_EXCEPT:
                if not fnmatch.fnmatch(username, assignment.username):
                    used_assignment = assignment
                    break
        if used_assignment is None:
            return None
        return used_assignment


class Assignment(models.Model):
    username_mode = models.IntegerField(choices=settings.ASSIGNMENT_CHOICES)
    username = models.CharField(max_length=255, blank=True)
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
            dict(settings.ASSIGNMENT_CHOICES)[self.username_mode],
            self.username,
        )

    objects = AssignmentManager()
