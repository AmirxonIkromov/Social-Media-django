# Generated by Django 4.1.2 on 2022-11-01 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id_user',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
