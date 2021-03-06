# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-28 23:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20180428_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow', label='\u6bb5\u843d')), (b'image_list_4', wagtail.wagtailcore.blocks.StructBlock([(b'image_list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='\u56fe\u7247')), (b'caption', wagtail.wagtailcore.blocks.CharBlock(label='\u56fe\u7247\u6807\u9898', max_length=255, required=False)), (b'page', wagtail.wagtailcore.blocks.PageChooserBlock(can_choose_root=True, label='\u94fe\u63a5\u5230\u9875\u9762', required=False))], label='\u56db\u5217\u56fe\u7247'), label='\u56db\u5217\u56fe\u7247'))], icon='image', label='\u56db\u5217\u56fe\u7247')), (b'image_list_3', wagtail.wagtailcore.blocks.StructBlock([(b'image_list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='\u56fe\u7247')), (b'caption', wagtail.wagtailcore.blocks.CharBlock(label='\u56fe\u7247\u6807\u9898', max_length=255, required=False)), (b'page', wagtail.wagtailcore.blocks.PageChooserBlock(can_choose_root=True, label='\u94fe\u63a5\u5230\u9875\u9762', required=False))], label='\u4e09\u5217\u56fe\u7247'), label='\u4e09\u5217\u56fe\u7247'))], icon='image', label='\u4e09\u5217\u56fe\u7247')), (b'link_list', wagtail.wagtailcore.blocks.StructBlock([(b'link_list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(label='\u6807\u9898', max_length=255, required=True)), (b'page', wagtail.wagtailcore.blocks.PageChooserBlock(can_choose_root=True, label='\u94fe\u63a5\u5230\u9875\u9762', required=False))], label='\u94fe\u63a5'), label='\u94fe\u63a5\u5217\u8868'))], icon='link', label='\u94fe\u63a5\u5217\u8868')), (b'html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='code', label='HTML\u4ee3\u7801'))], verbose_name='\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='simplepage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow', label='\u6bb5\u843d')), (b'image_list', wagtail.wagtailcore.blocks.StructBlock([(b'image_list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='\u56fe\u7247')), (b'caption', wagtail.wagtailcore.blocks.CharBlock(label='\u56fe\u7247\u6807\u9898', max_length=255, required=False)), (b'page', wagtail.wagtailcore.blocks.PageChooserBlock(can_choose_root=True, label='\u94fe\u63a5\u5230\u9875\u9762', required=False))], label='\u56fe\u7247')))], icon='image', label='\u56fe\u7247\u5217\u8868')), (b'html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='code', label='HTML\u4ee3\u7801'))]),
        ),
        migrations.AlterField(
            model_name='simplepage',
            name='intro',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='\u7b80\u8981\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='simplepage',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='\u7f29\u7565\u56fe'),
        ),
    ]
