# Generated by Django 4.0.6 on 2022-07-14 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='body',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='updated',
            new_name='modified',
        ),
    ]
