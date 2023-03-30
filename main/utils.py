from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon


def gerar_menu(usuario, ativo=None):
    side_menu_list = [
        {
            'name': 'Biblioteca',
            'app_label': 'main',
            'app_url': '/admin/main/',
            'has_module_perms': True,
            'models': []
        }
    ]
    if usuario.has_perm('main.change_autor'):
        is_active = True if ativo == 'autor' else False
        side_menu_list[0]['models'].append(
            {'name': 'Autores', 'object_name': 'Autores', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/autor/', 'add_url': '/admin/main/autor/add/', 'view_only': False, 'url': '/admin/main/autor/', 'model_str': 'main.cliente', 'icon': 'fas fa-user-tie', 'is_active': is_active}
        )
    if usuario.has_perm('main.change_categoria'):
        is_active = True if ativo == 'categoria' else False
        side_menu_list[0]['models'].append(
            {'name': 'Categorias', 'object_name': 'Categorias', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/categoria/', 'add_url': '/admin/main/categoria/add/', 'view_only': False, 'url': '/admin/main/categoria/', 'model_str': 'main.categoria', 'icon': 'fas fa-tag', 'is_active': is_active}
        )
    if usuario.has_perm('main.change_colecao'):
        is_active = True if ativo == 'colecao' else False
        side_menu_list[0]['models'].append(
            {'name': 'Coleções', 'object_name': 'Coleções', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/colecao/', 'add_url': '/admin/main/colecao/add/', 'view_only': False, 'url': '/admin/main/colecao/', 'model_str': 'main.colecao', 'icon': 'fas fa-tasks', 'is_active': is_active}
        )
    if usuario.has_perm('main.change_editora'):
        is_active = True if ativo == 'editora' else False
        side_menu_list[0]['models'].append(
            {'name': 'Editoras', 'object_name': 'Editoras', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/editora/', 'add_url': '/admin/main/editora/add/', 'view_only': False, 'url': '/admin/main/editora/', 'model_str': 'main.editora', 'icon': 'fas fa-university', 'is_active': is_active}
        )
    if usuario.has_perm('main.change_estante'):
        is_active = True if ativo == 'estante' else False
        side_menu_list[0]['models'].append(
            {'name': 'Estantes', 'object_name': 'Estantes', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/estante/', 'add_url': '/admin/main/estante/add/', 'view_only': False, 'url': '/admin/main/estante/', 'model_str': 'main.estante', 'icon': 'fas fa-bookmark', 'is_active': is_active}
        )
    if usuario.has_perm('main.change_idioma'):
        is_active = True if ativo == 'idioma' else False
        side_menu_list[0]['models'].append(
            {'name': 'Idiomas', 'object_name': 'Idiomas', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/idioma/', 'add_url': '/admin/main/idioma/add/', 'view_only': False, 'url': '/admin/main/idioma/', 'model_str': 'main.idioma', 'icon': 'fas fa-language', 'is_active': is_active}
        )
    if usuario.has_perm('main.change_livro'):
        is_active = True if ativo == 'livro' else False
        side_menu_list[0]['models'].append(
            {'name': 'Livros', 'object_name': 'Livros', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/livro/', 'add_url': '/admin/main/livro/add/', 'view_only': False, 'url': '/admin/main/livro/', 'model_str': 'main.livro', 'icon': 'fas fa-book', 'is_active': is_active}
        )
    if usuario.has_perm('main.add_leitura'):
        is_active = True if ativo == 'meus_livros' else False
        side_menu_list[0]['models'].append(
            {'name': 'Meus Livros Lidos', 'object_name': 'Meus Livros Lido', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'view_only': False, 'url': '/meus_livros_lidos/', 'model_str': 'main.livro', 'icon': 'fas fa-book-reader', 'is_active': is_active}
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
