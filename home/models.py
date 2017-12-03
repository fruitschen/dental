# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from PIL import Image as PILImage
from PIL import ExifTags

from django.db import models
from django.db.models.signals import post_save
from django import forms

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.models import Image as WagtailImage
from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, \
    RawHTMLBlock, PageChooserBlock, ListBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock

from modelcluster.fields import ParentalKey


# Global Streamfield definition


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class PagesRichTextBlock(StructBlock):
    content = RichTextBlock()


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = CharBlock(required=False, max_length=255)
    page = PageChooserBlock(can_choose_root=True, required=False)


class ImageListBlock(StructBlock):
    image_list = ListBlock(ImageBlock(label="Images"))


class PagesStreamBlock(StreamBlock):
    paragraph = RichTextBlock(icon="pilcrow")
    image_list = ImageListBlock(icon="image")


class HomePage(Page):
    parent_page_types = []


class SimplePage(Page):
    intro = RichTextField(blank=True)
    content = StreamField(
        PagesStreamBlock,
    )

    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    timestamp = models.DateTimeField(
        verbose_name=u'时间',
        blank=True,
        null=True
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    api_fields = ['intro', 'content', 'thumbnail', ]
    subpage_types = []

    def save(self, *args, **kwargs):
        result = super(SimplePage, self).save(*args, **kwargs)
        if self.first_published_at and self.timestamp and self.first_published_at > self.timestamp:
            self.first_published_at = self.timestamp
            self.save()

    class Meta:
        verbose_name = u'简单页面'


SimplePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('timestamp'),
    ImageChooserPanel('thumbnail'),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('content'),
]


class PersonBlock(StructBlock):
    photo = ImageChooserBlock(required=True)
    name = CharBlock()
    biography = RichTextBlock()

    class Meta:
        icon = 'user'


class DentistStreamBlock(StreamBlock):
    person = PersonBlock(icon="user")


class DentistsPage(Page):
    intro = RichTextField(blank=True)
    content = StreamField(
        DentistStreamBlock
    )

    timestamp = models.DateTimeField(
        verbose_name=u'时间',
        blank=True,
        null=True
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    api_fields = ['intro', 'content', ]
    subpage_types = []

    def save(self, *args, **kwargs):
        result = super(DentistsPage, self).save(*args, **kwargs)
        if self.first_published_at and self.timestamp and self.first_published_at > self.timestamp:
            self.first_published_at = self.timestamp
            self.save()

    class Meta:
        verbose_name = u'医生团队页面'


DentistsPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('timestamp'),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('content'),
]


# Category Page


class CategoryPage(Page):
    intro = RichTextField(blank=True)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'标题图片',
    )
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name = u'缩略图',
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    api_fields = ['intro', 'thumbnail']

    subpage_types = ['SimplePage']

    class Meta:
        verbose_name = u'分类页面'


CategoryPage.content_panels = [
    FieldPanel('title', classname="full title"),
    ImageChooserPanel('header_image'),
    ImageChooserPanel('thumbnail'),
    FieldPanel('intro', classname="full"),
]

