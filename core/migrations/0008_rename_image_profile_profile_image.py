# Generated by Django 3.2.12 on 2022-02-16 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_profile_bio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='profile_image',
        ),
    ]