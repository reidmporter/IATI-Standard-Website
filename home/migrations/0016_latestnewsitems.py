# Generated by Django 2.2.9 on 2020-02-26 11:27

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('home', '0015_remove_homepage_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestNewsItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('item', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='latest_news_items', to='home.HomePage')),
                ('page', models.ForeignKey(help_text='Page link for the item', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
