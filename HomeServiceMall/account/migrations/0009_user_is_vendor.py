# Generated by Django 3.2.5 on 2021-07-13 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210711_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_vendor',
            field=models.BooleanField(default=0, verbose_name='商贩'),
        ),
    ]