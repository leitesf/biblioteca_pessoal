# Generated by Django 4.1.7 on 2023-03-23 17:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_colecao_alter_livro_categoria_alter_livro_editora_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='ano',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ano de Publicação'),
        ),
        migrations.AddField(
            model_name='livro',
            name='paginas',
            field=models.IntegerField(blank=True, null=True, verbose_name='Páginas'),
        ),
        migrations.AddField(
            model_name='livro',
            name='sinopse',
            field=models.TextField(blank=True, verbose_name='Sinopse'),
        ),
        migrations.AddField(
            model_name='livro',
            name='subtitulo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Subtítulo'),
        ),
        migrations.CreateModel(
            name='Leitura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=datetime.date(2023, 3, 23), verbose_name='Data de Leitura')),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.livro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
    ]