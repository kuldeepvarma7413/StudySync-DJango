# Generated by Django 4.2.6 on 2023-12-02 01:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_user_email_verification_auth_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_email_verification',
            name='id',
        ),
        migrations.AlterField(
            model_name='user_email_verification',
            name='auth_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]