# Generated by Django 3.1.1 on 2020-11-18 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensagem',
            name='texto',
            field=models.CharField(max_length=250),
        ),
    ]
