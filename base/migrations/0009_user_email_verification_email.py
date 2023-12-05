# Generated by Django 4.2.6 on 2023-11-02 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_user_email_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_email_verification',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]