from datetime import datetime

from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from main.models import *


def gerar_menu(usuario, ativo=None):
    side_menu_list = [
        {
            'name': 'Biblioteca',
            'app_label': 'main',
            'app_url': '/admin/main/',
            'has_module_perms': True,
            'models': []
        },
        {
            'name': 'Games',
            'app_label': 'games',
            'app_url': '/admin/games/',
            'has_module_perms': True,
            'models': []
        }
    ]
    if usuario.has_perm('main.view_livro'):
        is_active = True if ativo == 'livro' else False
        side_menu_list[0]['models'].append(
            {'name': 'Livros', 'object_name': 'Livros', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/livro/', 'add_url': '/admin/main/livro/add/', 'view_only': False, 'url': '/admin/main/livro/', 'model_str': 'main.livro', 'icon': 'fas fa-book', 'is_active': is_active}
        )
    if usuario.has_perm('main.view_autor'):
        is_active = True if ativo == 'autor' else False
        side_menu_list[0]['models'].append(
            {'name': 'Autores', 'object_name': 'Autores', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/autor/', 'add_url': '/admin/main/autor/add/', 'view_only': False, 'url': '/admin/main/autor/', 'model_str': 'main.cliente', 'icon': 'fas fa-user-tie', 'is_active': is_active}
        )
    if usuario.has_perm('main.viewegoria'):
        is_active = True if ativo == 'categoria' else False
        side_menu_list[0]['models'].append(
            {'name': 'Categorias', 'object_name': 'Categorias', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/categoria/', 'add_url': '/admin/main/categoria/add/', 'view_only': False, 'url': '/admin/main/categoria/', 'model_str': 'main.categoria', 'icon': 'fas fa-tag', 'is_active': is_active}
        )
    if usuario.has_perm('main.viewolecao'):
        is_active = True if ativo == 'colecao' else False
        side_menu_list[0]['models'].append(
            {'name': 'Coleções', 'object_name': 'Coleções', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/colecao/', 'add_url': '/admin/main/colecao/add/', 'view_only': False, 'url': '/admin/main/colecao/', 'model_str': 'main.colecao', 'icon': 'fas fa-tasks', 'is_active': is_active}
        )
    if usuario.has_perm('main.viewditora'):
        is_active = True if ativo == 'editora' else False
        side_menu_list[0]['models'].append(
            {'name': 'Editoras', 'object_name': 'Editoras', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/editora/', 'add_url': '/admin/main/editora/add/', 'view_only': False, 'url': '/admin/main/editora/', 'model_str': 'main.editora', 'icon': 'fas fa-university', 'is_active': is_active}
        )
    if usuario.has_perm('main.viewestimo'):
        is_active = True if ativo == 'emprestimo' else False
        side_menu_list[0]['models'].append(
            {'name': 'Empréstimos', 'object_name': 'Empréstimos', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/emprestimo/', 'add_url': '/admin/main/emprestimo/add/', 'view_only': False, 'url': '/admin/main/emprestimo/', 'model_str': 'main.emprestimo', 'icon': 'fas fa-stamp', 'is_active': is_active}
        )
    if usuario.has_perm('main.viewstante'):
        is_active = True if ativo == 'estante' else False
        side_menu_list[0]['models'].append(
            {'name': 'Estantes', 'object_name': 'Estantes', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/estante/', 'add_url': '/admin/main/estante/add/', 'view_only': False, 'url': '/admin/main/estante/', 'model_str': 'main.estante', 'icon': 'fas fa-bookmark', 'is_active': is_active}
        )
    if usuario.has_perm('main.viewidioma'):
        is_active = True if ativo == 'idioma' else False
        side_menu_list[0]['models'].append(
            {'name': 'Idiomas', 'object_name': 'Idiomas', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/idioma/', 'add_url': '/admin/main/idioma/add/', 'view_only': False, 'url': '/admin/main/idioma/', 'model_str': 'main.idioma', 'icon': 'fas fa-language', 'is_active': is_active}
        )
    if usuario.has_perm('main.add_leitura'):
        is_active = True if ativo == 'meus_livros' else False
        side_menu_list[0]['models'].append(
            {'name': 'Meus Livros Lidos', 'object_name': 'Meus Livros Lidos', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'view_only': False, 'url': '/meus_livros_lidos/', 'model_str': 'main.livro', 'icon': 'fas fa-book-reader', 'is_active': is_active}
        )
    if usuario.has_perm('main.mesclar_autores'):
        is_active = True if ativo == 'mesclar_autores' else False
        side_menu_list[0]['models'].append(
            {'name': 'Mesclar Autores', 'object_name': 'Mesclar Autores', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'view_only': False, 'url': '/mesclar_autores/', 'model_str': 'main.autor', 'icon': 'fas fa-object-group', 'is_active': is_active}
        )
    if usuario.has_perm('main.mesclar_editoras'):
        is_active = True if ativo == 'mesclar_editoras' else False
        side_menu_list[0]['models'].append(
            {'name': 'Mesclar Editoras', 'object_name': 'Mesclar Editoras', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'view_only': False, 'url': '/mesclar_editoras/', 'model_str': 'main.editora', 'icon': 'fas fa-object-group', 'is_active': is_active}
        )
    if usuario.has_perm('main.view_jogos'):
        is_active = True if ativo == 'jogo' else False
        side_menu_list[1]['models'].append(
            {'name': 'Jogos', 'object_name': 'Jogos', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/games/jogo/', 'add_url': '/admin/games/jogo/add/', 'view_only': False, 'url': '/admin/games/jogo/', 'model_str': 'main.jogo', 'icon': 'fas fa-gamepad', 'is_active': is_active}
        )
    if usuario.has_perm('main.view_franquias'):
        is_active = True if ativo == 'franquia' else False
        side_menu_list[1]['models'].append(
            {'name': 'Franquias', 'object_name': 'Franquias', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/games/franquia/', 'add_url': '/admin/games/franquia/add/', 'view_only': False, 'url': '/admin/games/franquia/', 'model_str': 'main.franquia', 'icon': 'fas fa-layer-group', 'is_active': is_active}
        )
    if usuario.has_perm('main.view_generos'):
        is_active = True if ativo == 'genero' else False
        side_menu_list[1]['models'].append(
            {'name': 'Gêneros', 'object_name': 'Gêneros', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/games/genero/', 'add_url': '/admin/games/genero/add/', 'view_only': False, 'url': '/admin/games/genero/', 'model_str': 'main.genero', 'icon': 'fas fa-tag', 'is_active': is_active}
        )
    if usuario.has_perm('main.view_lojas'):
        is_active = True if ativo == 'loja' else False
        side_menu_list[1]['models'].append(
            {'name': 'Lojas', 'object_name': 'Lojas', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/games/loja/', 'add_url': '/admin/games/loja/add/', 'view_only': False, 'url': '/admin/games/loja/', 'model_str': 'main.loja', 'icon': 'fas fa-store', 'is_active': is_active}
        )
    if usuario.has_perm('main.view_plataformas'):
        is_active = True if ativo == 'plataforma' else False
        side_menu_list[1]['models'].append(
            {'name': 'Plataformas', 'object_name': 'Plataformas', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/games/plataforma/', 'add_url': '/admin/games/plataforma/add/', 'view_only': False, 'url': '/admin/games/plataforma/', 'model_str': 'main.plataforma', 'icon': 'fas fa-globe', 'is_active': is_active}
        )
    if usuario.is_superuser:
        is_active = True if ativo == 'usuario' else False
        side_menu_list.append({
            'name': 'Autenticação e Autorização',
            'app_label': 'auth',
            'app_url': '/admin/auth/',
            'has_module_perms': True,
            'models':
                [
                    {
                        'name': 'Grupos',
                        'object_name': 'Group',
                        'perms':
                            {
                                'add': True, 'change': True, 'delete': True, 'view': True
                            },
                        'admin_url': '/admin/auth/group/',
                        'add_url': '/admin/auth/group/add/',
                        'view_only': False,
                        'url': '/admin/auth/group/',
                        'model_str': 'auth.group',
                        'icon': 'fas fa-users'
                    },
                    {
                        'name': 'Usuários',
                        'url': '/admin/main/usuario/',
                        'children': None,
                        'new_window': False,
                        'icon': 'fas fa-user',
                        'is_active': is_active
                    },
                    {
                        'name': 'Configuração do Sistema',
                        'url': '/admin/main/configuracaosistema/',
                        'children': None,
                        'new_window': False,
                        'icon': 'fas fa-wrench'
                    },
                ], 'icon': 'fas fa-users-cog'
        }
        )
    return side_menu_list


def get_badge_boolean(valor):
    return mark_safe('<span class="badge badge-success">Sim</span>' if valor else '<span class="badge badge-danger">Não</span>')


def montar_header_do_skoob(usuario):
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

def importar_skoob_usuario(usuario):
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
        usuario_principal = configuracao.usuario_principal == usuario

        if usuario_principal:
            dados = requests.get(url='https://prd-api.skoob.com.br/api/v1/bookshelf?limit=1000&page=1&filter=owned', headers=montar_header_do_skoob(usuario))
            dados = dados.json()
            print("Importando livros do usuário principal")
            livros_adicionados=[]
            for item in tqdm(dados['items']):
                if not Livro.objects.filter(skoob_id=item['edition_id']).exists():
                    livro = Livro()

                    dados_livro = requests.get(url='https://prd-api.skoob.com.br/api/v1/book/{}'.format(item['edition_id']), headers=montar_header_do_skoob(usuario)).json()

                    livro.titulo = item['title']
                    livro.ano = item['year'] if item['year'] else None
                    if Editora.objects.filter(nome=item['publisher']).exists():
                        livro.editora = Editora.objects.get(nome=item['publisher'])
                    else:
                        livro.editora = Editora.objects.create(
                            nome=item['publisher']
                        )
                    livro.sinopse = dados_livro['about']['description']
                    if dados_livro['subtitle']:
                        livro.subtitulo = dados_livro['subtitle']
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
                            usuario=usuario,
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
        else:
            livros_adicionados = []

        dados = requests.get(url='https://prd-api.skoob.com.br/api/v1/bookshelf?limit=1000&page=1&filter=read', headers=montar_header_do_skoob(usuario))
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
        return True, livros_adicionados, livros_lidos
    return False
