# Generated by Django 3.0.4 on 2020-04-01 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200401_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='read_number',
            field=models.IntegerField(default=0),
        ),
    ]