# Generated by Django 3.2.12 on 2022-02-16 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_image_profile_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='email',
        ),
    ]
