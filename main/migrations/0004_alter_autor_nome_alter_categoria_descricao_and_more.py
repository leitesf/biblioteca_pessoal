# Generated by Django 4.1.7 on 2023-03-30 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_usuario_skoob_user_configuracaosistema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autor',
            name='nome',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='descricao',
            field=models.CharField(max_length=50, unique=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='colecao',
            name='descricao',
            field=models.CharField(max_length=50, unique=True, verbose_name='Coleção'),
        ),
        migrations.AlterField(
            model_name='configuracaosistema',
            name='usuario_principal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário Principal'),
        ),
        migrations.AlterField(
            model_name='editora',
            name='nome',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='idioma',
            name='nome',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='livro',
            name='skoob_id',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='ID no Skoob'),
        ),
        migrations.AlterUniqueTogether(
            name='estante',
            unique_together={('descricao', 'comodo')},
        ),
    ]
