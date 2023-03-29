from datetime import datetime

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from main.models import *


class Command(BaseCommand):
    help = "Converte um arquivo livros.json baixado do skoob em livros cadastrados no sistema"

    def handle(self, *args, **options):
        with transaction.atomic():
            estante = Estante.objects.get_or_create(
                descricao="A definir"
            )[0]
            categoria = Categoria.objects.get_or_create(
                descricao='A definir'
            )[0]
            idioma = Idioma.objects.get_or_create(
                nome='Português'
            )[0]
            usuario = Usuario.objects.get(username='rafael')

            dados = requests.get(
                "https://www.skoob.com.br/v1/bookcase/books/142377/shelf_id:6/page:0/limit:1000").json()

            for item in dados['response']:
                if not Livro.objects.filter(skoob_id=item['edicao']['id']).exists():
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
                    livro.skoob_id = item['edicao']['id']
                    autores = item['edicao']['autor'].strip().split(',')
                    if ' ' in autores:
                        autores.remove(' ')
                    if '' in autores:
                        autores.remove('')
                    livro.autor_principal = Autor.objects.get_or_create(nome=autores[0])[0]

                    livro.save()
                    if len(autores) > 1:
                        for autor in autores[1:]:
                            livro.autores_secundarios.add(
                                Autor.objects.get_or_create(nome=autor)[0]
                            )
                    if 'dt_leitura' in item and item['dt_leitura']:
                        Leitura.objects.create(
                            usuario=usuario,
                            livro=livro,
                            data=datetime.strptime(item['dt_leitura'], '%Y-%m-%d %H:%M:%S').date()
                        )

                    capa = requests.get(item['edicao']['capa_media'])
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(capa.content)
                    img_temp.flush()
                    livro.capa.save('capa-{}.jpg'.format(livro.id), File(img_temp), save=True)
                    print(livro.id)
