# Generated by Django 3.2.5 on 2021-07-16 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_applyforshop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='star',
            field=models.IntegerField(blank=True, default=5, null=True, verbose_name='店铺星级'),
        ),
    ]