# Generated by Django 2.2.9 on 2020-03-17 15:30

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.blocks.static_block
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primarymenulinks',
            name='meganav',
            field=wagtail.core.fields.StreamField([('type_a', wagtail.core.blocks.StructBlock([('highlight', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(help_text='Page for title and link')), ('description_en', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [en]')), ('description_fr', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [fr]', required=False))])), ('columns_label', wagtail.core.blocks.static_block.StaticBlock(admin_text='\n            <div class="help-block help-info">\n                <p>\n                    <strong>Columns</strong><br>\n                    Column elements for the meganav module.<br>\n                    Maximum number of items: 4\n                </p>\n            </div>\n            ')), ('columns', wagtail.core.blocks.StreamBlock([('page_list', wagtail.core.blocks.StructBlock([('use_first_page_as_title', wagtail.core.blocks.BooleanBlock(help_text='Optional: if checked, the first page in the list will be displayed as a title, overriding any plain text title below', required=False)), ('title_en', wagtail.core.blocks.CharBlock(help_text='Optional: plain text title for the page list', label='Title [en]', required=False)), ('title_fr', wagtail.core.blocks.CharBlock(help_text='Optional: plain text title for the page list', label='Title [fr]', required=False)), ('description_en', wagtail.core.blocks.CharBlock(help_text='Optional: description for the page list', label='Description [en]', required=False)), ('description_fr', wagtail.core.blocks.CharBlock(help_text='Optional: description for the page list', label='Description [fr]', required=False)), ('page_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock())]), label='Pages'))])), ('nested_page_list', wagtail.core.blocks.StructBlock([('groups', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(help_text='Optional: top level page for the group', label='Top level page', required=False)), ('title_en', wagtail.core.blocks.CharBlock(help_text='Optional: plain text title for the page group', label='Title [en]', required=False)), ('title_fr', wagtail.core.blocks.CharBlock(help_text='Optional: plain text title for the page group', label='Title [fr]', required=False)), ('page_group', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock())]), help_text='Optional: group of sub pages, displayed as an indented list', required=False))])))]))], max_num=4, min_num=0, required=False))])), ('type_b', wagtail.core.blocks.StructBlock([('highlight', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(help_text='Page for title and link')), ('description_en', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [en]')), ('description_fr', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [fr]', required=False))])), ('columns_label', wagtail.core.blocks.static_block.StaticBlock(admin_text='\n            <div class="help-block help-info">\n                <p>\n                    <strong>Columns</strong><br>\n                    Column elements for the meganav module.<br>\n                    Maximum number of items: 2\n                </p>\n            </div>\n            ')), ('columns', wagtail.core.blocks.StreamBlock([('page_list', wagtail.core.blocks.StructBlock([('use_first_page_as_title', wagtail.core.blocks.BooleanBlock(help_text='Optional: if checked, the first page in the list will be displayed as a title, overriding any plain text title below', required=False)), ('title_en', wagtail.core.blocks.CharBlock(help_text='Optional: plain text title for the page list', label='Title [en]', required=False)), ('title_fr', wagtail.core.blocks.CharBlock(help_text='Optional: plain text title for the page list', label='Title [fr]', required=False)), ('description_en', wagtail.core.blocks.CharBlock(help_text='Optional: description for the page list', label='Description [en]', required=False)), ('description_fr', wagtail.core.blocks.CharBlock(help_text='Optional: description for the page list', label='Description [fr]', required=False)), ('page_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock())]), label='Pages'))])), ('featured', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(help_text='Page for title and link')), ('description_en', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [en]')), ('description_fr', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [fr]', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Optional: image for the module. If not selected, the page image will be used, or a fallback if not available', required=False)), ('secondary_page', wagtail.core.blocks.PageChooserBlock(help_text='Optional: secondary page link', required=False)), ('link_label_en', wagtail.core.blocks.CharBlock(help_text='Optional: label for the secondary page link', label='Link label [en]', required=False)), ('link_label_fr', wagtail.core.blocks.CharBlock(help_text='Optional: label for the secondary page link', label='Link label [fr]', required=False))]))], block_counts={'featured': {'max_num': 1}, 'page_list': {'max_num': 1}}, max_num=2, min_num=0, required=False))])), ('type_c', wagtail.core.blocks.StructBlock([('highlight', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(help_text='Page for title and link')), ('description_en', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [en]')), ('description_fr', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [fr]', required=False))])), ('columns_label', wagtail.core.blocks.static_block.StaticBlock(admin_text='\n            <div class="help-block help-info">\n                <p>\n                    <strong>Columns</strong><br>\n                    Column elements for the meganav module.<br>\n                    Maximum number of items: 7\n                </p>\n            </div>\n            ')), ('columns', wagtail.core.blocks.StreamBlock([('focus_item', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(help_text='Page for title and link')), ('description_en', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [en]')), ('description_fr', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [fr]', required=False)), ('external_url', wagtail.core.blocks.URLBlock(help_text='Optional: external URL for the secondary link. Defaults to the selected page link', required=False)), ('link_label_en', wagtail.core.blocks.CharBlock(help_text='Label for the secondary page link', label='Link label [en]')), ('link_label_fr', wagtail.core.blocks.CharBlock(help_text='Label for the secondary page link', label='Link label [fr]', required=False)), ('use_button_style', wagtail.core.blocks.BooleanBlock(help_text='Optional: if checked, the secondary link will display as a button', required=False))])), ('page_list', wagtail.core.blocks.StructBlock([('use_first_page_as_title', wagtail.core.blocks.BooleanBlock(help_text='Optional: if checked, the first page in the list will be displayed as a title, overriding any plain text title below', required=False)), ('title_en', wagtail.core.blocks.CharBlock(help_text='Optional: plain text title for the page list', label='Title [en]', required=False)), ('title_fr', wagtail.core.blocks.CharBlock(help_text='Optional: plain text title for the page list', label='Title [fr]', required=False)), ('description_en', wagtail.core.blocks.CharBlock(help_text='Optional: description for the page list', label='Description [en]', required=False)), ('description_fr', wagtail.core.blocks.CharBlock(help_text='Optional: description for the page list', label='Description [fr]', required=False)), ('page_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock())]), label='Pages'))])), ('secondary_highlight', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(help_text='Page for title and link')), ('description_en', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [en]')), ('description_fr', wagtail.core.blocks.TextBlock(help_text='Description for the module', label='Description [fr]', required=False)), ('link_label_en', wagtail.core.blocks.CharBlock(help_text='Label for the page link button', label='Link label [en]')), ('link_label_fr', wagtail.core.blocks.CharBlock(help_text='Label for the page link button', label='Link label [fr]', required=False))]))], block_counts={'focus_item': {'max_num': 5}, 'page_list': {'max_num': 1}, 'secondary_highlight': {'max_num': 1}}, max_num=7, min_num=0, required=False))]))], blank=True),
        ),
    ]
