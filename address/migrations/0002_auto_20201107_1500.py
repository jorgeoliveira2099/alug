# Generated by Django 3.1.1 on 2020-11-07 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dados_usuario',
            name='cep',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
