# Generated by Django 3.1.1 on 2020-11-14 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoSala', models.CharField(max_length=20, unique=True)),
                ('nomeSala', models.CharField(blank=True, max_length=200, null=True)),
                ('locador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_locador', to=settings.AUTH_USER_MODEL)),
                ('locatario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_locatario', to=settings.AUTH_USER_MODEL)),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=80)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Chat.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
