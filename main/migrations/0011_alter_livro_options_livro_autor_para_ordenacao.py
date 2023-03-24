# Generated by Django 4.1.7 on 2023-03-24 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_livro_colecao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='livro',
            options={'ordering': ['autor_para_ordenacao', 'titulo'], 'verbose_name': 'Livro', 'verbose_name_plural': 'Livros'},
        ),
        migrations.AddField(
            model_name='livro',
            name='autor_para_ordenacao',
            field=models.CharField(default='', max_length=100, verbose_name='Autor para ordenação'),
            preserve_default=False,
        ),
    ]
