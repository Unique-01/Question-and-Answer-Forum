# Generated by Django 3.2.12 on 2022-05-04 08:59

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_content_answer_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Your Answer'),
        ),
    ]
