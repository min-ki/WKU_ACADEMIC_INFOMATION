# Generated by Django 2.0.7 on 2018-08-17 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_at',)},
        ),
    ]
