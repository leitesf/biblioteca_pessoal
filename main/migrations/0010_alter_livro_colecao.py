# Generated by Django 4.1.7 on 2023-03-24 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_autor_options_alter_categoria_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='colecao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.colecao', verbose_name='Coleção'),
        ),
    ]
