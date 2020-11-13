# Generated by Django 3.1.1 on 2020-11-13 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20201107_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cidade',
            field=models.CharField(default='Recife', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='estado',
            field=models.CharField(default='Pernambuco', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='condicoesUso',
            field=models.TextField(verbose_name=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='descricao',
            field=models.TextField(verbose_name=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='nome',
            field=models.CharField(max_length=100, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='preco',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name=''),
        ),
    ]
