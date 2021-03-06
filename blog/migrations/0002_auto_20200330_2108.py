# Generated by Django 3.0.4 on 2020-03-30 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-create_time']},
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=30, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='blogtype',
            name='type_name',
            field=models.CharField(max_length=15, verbose_name='分类'),
        ),
    ]
