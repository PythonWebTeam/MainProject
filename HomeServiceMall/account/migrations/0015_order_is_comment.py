# Generated by Django 3.2.5 on 2021-07-15 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_service_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_comment',
            field=models.BooleanField(default=False, verbose_name='订单评价状态'),
        ),
    ]
