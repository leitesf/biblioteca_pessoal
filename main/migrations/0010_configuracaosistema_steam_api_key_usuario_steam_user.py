# Generated by Django 4.1.7 on 2023-04-18 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_autor_nacionalidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaosistema',
            name='steam_api_key',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Chave da API do Steam'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='steam_user',
            field=models.IntegerField(blank=True, null=True, verbose_name='Usuário na Steam'),
        ),
    ]