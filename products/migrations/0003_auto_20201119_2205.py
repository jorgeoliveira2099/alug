# Generated by Django 3.1.1 on 2020-11-20 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20201118_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='preco',
            field=models.CharField(max_length=13, verbose_name=''),
        ),
    ]
