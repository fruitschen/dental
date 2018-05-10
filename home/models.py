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

class SimpleImageBlock(StructBlock):
    image = ImageChooserBlock(label=u"图片")
    caption = CharBlock(required=False, max_length=255, label=u"图片标题")


class ImageBlock(StructBlock):
    image = ImageChooserBlock(label=u"图片")
    caption = CharBlock(required=False, max_length=255, label=u"图片标题")
    page = PageChooserBlock(can_choose_root=True, required=False, label=u"链接到页面")


class ImageListBlock(StructBlock):
    image_list = ListBlock(ImageBlock(label="图片"))


class PagesStreamBlock(StreamBlock):
    paragraph = RichTextBlock(icon="pilcrow", label=u'段落')
    image_list = ImageListBlock(icon="image", label=u'图片列表')
    html = RawHTMLBlock(icon="code", label=u'HTML代码')


# HomePage Streamfield definition

class HPFiveColImageListBlock(StructBlock):
    image_list = ListBlock(ImageChooserBlock(label=u"图片"))


class FourColImageListBlock(StructBlock):
    image_list = ListBlock(ImageBlock(label=u"四列图片"), label=u'四列图片')


class ThreeColImageListBlock(StructBlock):
    image_list = ListBlock(ImageBlock(label=u"三列图片"), label=u'三列图片')


class Carousel(StructBlock):
    image_list = ListBlock(SimpleImageBlock(label=u"幻灯片图片"), label=u'幻灯片图片')


class TwoColImageBlock(StructBlock):
    image = ImageChooserBlock(label=u"图片")
    desc1 = CharBlock(required=False, max_length=255, label=u"描述1")
    desc2 = CharBlock(required=False, max_length=255, label=u"描述2")
    link_text = CharBlock(required=False, max_length=255, label=u"链接文字")
    page = PageChooserBlock(can_choose_root=True, required=False, label=u"链接到页面")


class TwoColImageListBlock(StructBlock):
    image_list = ListBlock(TwoColImageBlock(label=u"两列图片"), label=u'两列图片')


class LinkItem(StructBlock):
    title = CharBlock(required=True, max_length=255, label=u"标题")
    page = PageChooserBlock(can_choose_root=True, required=False, label=u"链接到页面")


class LinkList(StructBlock):
    link_list = ListBlock(LinkItem(label=u"链接"), label=u'链接列表')


class OverlapDesign(StructBlock):
    title = CharBlock(required=True, max_length=255, label=u"大标题")
    subtitle = CharBlock(required=True, max_length=255, label=u"小标题")
    text = TextBlock(required=True, label=u'段落')


class HomePagesStreamBlock(StreamBlock):
    paragraph = RichTextBlock(icon="pilcrow", label=u'段落')
    image_list_4 = FourColImageListBlock(icon="image", label=u"四列图片")
    image_list_3 = ThreeColImageListBlock(icon="image", label=u"三列图片")
    image_list_2 = TwoColImageListBlock(icon="image", label=u"两列图片")
    link_list = LinkList(icon="link", label=u"链接列表")
    html = RawHTMLBlock(icon="code", label=u'HTML代码')
    overlap = OverlapDesign(icon="pilcrow", label=u"大小标题模块")
    quote = TextBlock(icon = "openquote", label=u'引用')
    image_list_5 = HPFiveColImageListBlock(icon="image", label=u"主页五列图片")
    carousel = Carousel(icon="image", label=u"幻灯片图片")


class HomePage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'标题图片',
    )
    content = StreamField(
        HomePagesStreamBlock,
        verbose_name=u'内容',
    )

    parent_page_types = []


HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    ImageChooserPanel('header_image'),
    StreamFieldPanel('content'),
]


class SimplePage(Page):
    intro = RichTextField(blank=True, verbose_name="简要内容")
    content = StreamField(
        PagesStreamBlock,
    )

    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=u'缩略图',
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

