# Generated by Django 3.2.5 on 2021-07-11 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_emailverifyrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='star',
            field=models.IntegerField(blank=True, null=True, verbose_name='星级'),
        ),
    ]