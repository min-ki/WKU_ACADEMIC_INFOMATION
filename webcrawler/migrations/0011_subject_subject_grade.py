# Generated by Django 2.0.7 on 2018-07-19 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcrawler', '0010_auto_20180719_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='subject_grade',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
