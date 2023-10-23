# Generated by Django 4.2.5 on 2023-10-15 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseCode', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=2)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
