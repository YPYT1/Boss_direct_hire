# Generated by Django 2.2.14 on 2024-01-15 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='count',
            field=models.IntegerField(default=1, verbose_name='点击次数'),
        ),
    ]
