from django.core.management.base import BaseCommand

import json
from datetime import datetime

from django.db import transaction

from main.models import *

class Command(BaseCommand):
    help = "Converte um arquivo livros.json baixado do skoob em livros cadastrados no sistema"

    def handle(self, *args, **options):
        with transaction.atomic():
            estante = Estante.objects.first()
            categoria = Categoria.objects.first()
            idioma = Idioma.objects.first()
            usuario = Usuario.objects.get(username='rafael')

            with open('livros.json') as data_file:
                dados = json.load(data_file)

            for item in dados['response']:
                livro = Livro()
                livro.titulo = item['edicao']['titulo']
                livro.subtitulo = item['edicao']['subtitulo'] if item['edicao']['subtitulo'] else None
                livro.ano = item['edicao']['ano']
                if Editora.objects.filter(nome=item['edicao']['editora']).exists():
                    livro.editora = Editora.objects.get(nome=item['edicao']['editora'])
                else:
                    livro.editora = Editora.objects.create(
                        nome=item['edicao']['editora']
                    )
                livro.categoria = categoria
                livro.estante = estante
                livro.idioma = idioma
                livro.sinopse = item['edicao']['sinopse']
                livro.paginas = item['edicao']['paginas']
                livro.save()
                autores = item['edicao']['autor'].strip().split(',')
                for autor in autores:
                    if Autor.objects.filter(nome=autor).exists():
                        livro.autores.add(Autor.objects.get(nome=autor))
                    else:
                        livro.autores.add(
                            Autor.objects.create(nome=autor)
                        )
                if 'dt_leitura' in item and item['dt_leitura']:
                    Leitura.objects.create(
                        usuario=usuario,
                        livro=livro,
                        data=datetime.strptime(item['dt_leitura'], '%Y-%m-%d %H:%M:%S').date()
                    )
