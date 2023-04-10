# Generated by Django 4.1.7 on 2023-04-10 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_autor_nome_alter_categoria_descricao_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'ordering': ['nome'], 'permissions': [('mesclar_autores', 'Pode mesclar autores')], 'verbose_name': 'Autor', 'verbose_name_plural': 'Autores'},
        ),
        migrations.AlterModelOptions(
            name='editora',
            options={'ordering': ['nome'], 'permissions': [('mesclar_editoras', 'Pode mesclar editoras')], 'verbose_name': 'Editora', 'verbose_name_plural': 'Editoras'},
        ),
        migrations.AlterModelOptions(
            name='leitura',
            options={'ordering': ['livro__autor_principal__nome_ordenado', 'livro__titulo', 'data'], 'verbose_name': 'Leitura', 'verbose_name_plural': 'Leituras'},
        ),
    ]
