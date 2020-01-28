"""Model definitions for the iati_standard app."""

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from wagtail.snippets.models import register_snippet

from home.models import AbstractContentPage, DefaultPageHeaderImageMixin

from iati_standard.panels import ReferenceDataPanel


class IATIStandardPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for the IATI Standard Page, a landing page for IATI reference."""

    parent_page_types = ['home.HomePage']
    subpage_types = []

    repo = models.URLField(
        help_text='Git repo URL',
        blank=True,
        null=True
    )

    live_tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
        blank=True,
        null=True
    )

    multilingual_field_panels = DefaultPageHeaderImageMixin.multilingual_field_panels + [ReferenceDataPanel()]


@register_snippet
class ReferenceData(models.Model):

    class Meta:
        ordering = ['json_path']
        verbose_name_plural = 'Reference data'
        unique_together = ['json_path', 'language', 'tag']

    json_path = models.TextField(
        null=True,
        blank=True,
        help_text='Folder path of JSON object'
    )

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    version = models.CharField(
        max_length=255,
        help_text='IATI version',
        null=True,
        blank=True
    )

    language = models.CharField(
        max_length=255,
        help_text='Language',
        null=True,
        blank=True
    )

    parent_path = models.TextField(
        null=True,
        blank=True,
        help_text='Parent path of object'
    )

    data = JSONField(blank=True, null=True)

    @cached_property
    def name(self):
        return self.json_path.split("/")[-1]

    @cached_property
    def reference_type(self):
        return self.json_path.split("/")[1]

    def __str__(self):
        return self.json_path

    def save(self, *args, **kwargs):
        self.parent_path = "/".join(self.json_path.split("/")[:-1])
        super(ReferenceData, self).save(*args, **kwargs)


class ActivityStandardPage(DefaultPageHeaderImageMixin, AbstractContentPage):
    """A model for reference to the Activity Standard"""

    parent_page_types = ['iati_standard.IATIStandardPage', 'iati_standard.ActivityStandardPage']
    sub_page_types = ['iati_standard.ActivityStandardPage']

    json_path = models.TextField(
        null=True,
        blank=True,
        help_text='Folder path of JSON object'
    )

    tag = models.CharField(
        max_length=255,
        help_text='Associated git release tag',
    )

    data = JSONField(blank=True, null=True)

    has_been_recursed = models.BooleanField(default=False)

    translation_fields = AbstractContentPage.translation_fields + ["data"]

    @cached_property
    def parent_path(self):
        return "/".join(self.json_path.split("/")[:-1])

    @cached_property
    def name(self):
        return self.json_path.split("/")[-1]

    @cached_property
    def version(self):
        return self.json_path.split("/")[0]
