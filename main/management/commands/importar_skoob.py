from datetime import datetime

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from main.models import *


class Command(BaseCommand):
    help = "Converte um arquivo livros.json baixado do skoob em livros cadastrados no sistema"

    def montar_header(self,usuario):
        return {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,en-US;q=0.6",
            "authorization": usuario.skoob_authentication,
            "content-type": "application/json",
            # "if-none-match": 'W/"hnVLAmB6W56WSP9o4Hj2RwyAeuQ="',  # Commented out to get fresh data instead of 304
            "origin": "https://www.skoob.com.br",
            "referer": "https://www.skoob.com.br/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }

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
            configuracao = ConfiguracaoSistema.objects.first()
            usuario_principal = configuracao.usuario_principal

            dados = requests.get(url='https://prd-api.skoob.com.br/api/v1/bookshelf?limit=1000&page=1&filter=owned', headers=self.montar_header(usuario_principal))
            dados = dados.json()
            print("Importando livros do usuário principal")
            livros_adicionados=[]
            for item in tqdm(dados['items']):
                if not Livro.objects.filter(skoob_id=item['edition_id']).exists():
                    livro = Livro()
                    livro.titulo = item['title']
                    livro.ano = item['year'] if item['year'] else None
                    if Editora.objects.filter(nome=item['publisher']).exists():
                        livro.editora = Editora.objects.get(nome=item['publisher'])
                    else:
                        livro.editora = Editora.objects.create(
                            nome=item['publisher']
                        )
                    livro.categoria = categoria
                    livro.estante = estante
                    livro.idioma = idioma
                    livro.paginas = item['pages']
                    livro.skoob_id = item['edition_id']
                    autores = item['author'].strip().split(',')
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
                    if 'finished_at' in item and item['finished_at']:
                        Leitura.objects.create(
                            usuario=usuario_principal,
                            livro=livro,
                            data=datetime.strptime(item['finished_at'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
                        )
                    link_da_capa = item['cover_filename'] 
                    if link_da_capa:
                        capa = requests.get(item['cover_filename'])
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(capa.content)
                        img_temp.flush()
                        livro.capa.save('capa-{}.jpg'.format(livro.id), File(img_temp), save=True)
                    livros_adicionados.append(livro)
            for livro in livros_adicionados:
                print('Livro adicionado: {} ({})'.format(livro.titulo, livro.autor_principal))
            for usuario in Usuario.objects.filter(skoob_authentication__isnull=False):
                dados = requests.get(url='https://prd-api.skoob.com.br/api/v1/bookshelf?limit=1000&page=1&filter=read', headers=self.montar_header(usuario_principal))
                dados = dados.json()
                print("Buscando livros lidos por {}".format(usuario.get_full_name()))
                livros_lidos=[]
                for item in tqdm(dados['items']):
                    if Livro.objects.filter(skoob_id=item['edition_id']).exists() and not \
                            Leitura.objects.filter(usuario=usuario, livro__skoob_id=item['edition_id']).exists():
                        if 'finished_at' in item and item['finished_at']:
                            livro = Livro.objects.get(skoob_id=item['edition_id'])
                            Leitura.objects.create(
                                usuario=usuario,
                                livro=livro,
                                data=datetime.strptime(item['finished_at'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
                            )
                            livros_lidos.append(livro)
                for livro in livros_lidos:
                    print("Livro marcado como lido: {} ({})".format(livro.titulo, livro.autor_principal))
