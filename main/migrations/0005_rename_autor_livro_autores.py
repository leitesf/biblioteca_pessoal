# Generated by Django 4.1.7 on 2023-03-22 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_livro_autor_livro_autor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livro',
            old_name='autor',
            new_name='autores',
        ),
    ]