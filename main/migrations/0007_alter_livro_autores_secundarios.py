# Generated by Django 4.1.7 on 2023-04-14 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_emprestimo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='autores_secundarios',
            field=models.ManyToManyField(blank=True, null=True, related_name='livros_como_secundario', to='main.autor', verbose_name='Autores Secundários'),
        ),
    ]
