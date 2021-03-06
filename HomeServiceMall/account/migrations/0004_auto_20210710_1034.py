# Generated by Django 3.2.5 on 2021-07-10 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_user_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.IntegerField(blank=True, null=True, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='user',
            name='district',
            field=models.IntegerField(blank=True, null=True, verbose_name='区县'),
        ),
        migrations.AlterField(
            model_name='user',
            name='province',
            field=models.IntegerField(blank=True, null=True, verbose_name='省份'),
        ),
    ]
