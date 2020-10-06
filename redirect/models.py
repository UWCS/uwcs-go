from django.conf import settings
from django.db import models
from django.contrib.sites.shortcuts import get_current_site

# Create your models here.
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe


class Redirect(models.Model):
    source = models.CharField(max_length=50)
    sink = models.URLField(max_length=250)
    permanent = models.BooleanField(default=False)
    usages = models.PositiveIntegerField(default=0, help_text="The number of times that link has been used")

    def __str__(self):
        return self.source

    def get_absolute_url(self):
        return reverse("redirect", kwargs={"source": self.source})

    @property
    def url(self):
        try:
            url_ = settings.DEFAULT_PROTOCOL + settings.DEFAULT_DOMAIN + self.get_absolute_url()
            return mark_safe('<a href="{}">{}</a>'.format(url_, url_))
        except NoReverseMatch:
            return "-"
