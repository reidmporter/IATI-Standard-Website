# Generated by Django 2.2.9 on 2020-02-21 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_testimonialitems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='testimonial',
        ),
    ]
