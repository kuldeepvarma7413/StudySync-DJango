# Generated by Django 4.2.6 on 2023-12-15 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_cafiles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cafiles',
            old_name='file',
            new_name='files',
        ),
    ]
