# Generated by Django 4.1.7 on 2023-04-18 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, unique=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Gênero',
                'verbose_name_plural': 'Gêneros',
                'ordering': ['descricao'],
            },
        ),
        migrations.CreateModel(
            name='Loja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Loja',
                'verbose_name_plural': 'Lojas',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Plataforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Plataforma',
                'verbose_name_plural': 'Plataformas',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Jogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo')),
                ('tipo', models.CharField(choices=[('Físico', 'Físico'), ('Digital', 'Digital')], default='Digital', max_length=7, verbose_name='Tipo')),
                ('steam_id', models.IntegerField(blank=True, null=True, unique=True, verbose_name='ID no Steam')),
                ('capa', models.ImageField(blank=True, null=True, upload_to='capas_jogo', verbose_name='Capa do Jogo')),
                ('genero', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='games.genero', verbose_name='Gênero')),
                ('loja', models.ManyToManyField(blank=True, related_name='jogos', to='games.loja', verbose_name='Loja')),
                ('plataforma', models.ManyToManyField(blank=True, related_name='jogos', to='games.plataforma', verbose_name='Plataformas')),
            ],
            options={
                'verbose_name': 'Jogo',
                'verbose_name_plural': 'Jogos',
                'ordering': ['titulo'],
            },
        ),
    ]
