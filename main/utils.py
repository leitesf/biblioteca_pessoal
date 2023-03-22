from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

#
def gerar_menu(usuario):
    side_menu_list = [
        {
            'name': 'Biblioteca Pessoal',
            'app_label': 'main',
            'app_url': '/admin/main/',
            'has_module_perms': True,
            'models': []
        }
    ]
    if usuario.has_perm('main.change_autor'):
        side_menu_list[0]['models'].append(
            {'name': 'Autores', 'object_name': 'Autores', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/autor/', 'add_url': '/admin/main/autor/add/', 'view_only': False, 'url': '/admin/main/autor/', 'model_str': 'main.cliente', 'icon': 'fas fa-user-tie'}
        )
    if usuario.has_perm('main.change_categoria'):
        side_menu_list[0]['models'].append(
            {'name': 'Categorias', 'object_name': 'Categorias', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/categoria/', 'add_url': '/admin/main/categoria/add/', 'view_only': False, 'url': '/admin/main/categoria/', 'model_str': 'main.categoria', 'icon': 'fas fa-tag'}
        )
    if usuario.has_perm('main.change_editora'):
        side_menu_list[0]['models'].append(
            {'name': 'Editoras', 'object_name': 'Editoras', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/editora/', 'add_url': '/admin/main/editora/add/', 'view_only': False, 'url': '/admin/main/editora/', 'model_str': 'main.editora', 'icon': 'fas fa-university'}
        )
    if usuario.has_perm('main.change_estante'):
        side_menu_list[0]['models'].append(
            {'name': 'Estantes', 'object_name': 'Estantes', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/estante/', 'add_url': '/admin/main/estante/add/', 'view_only': False, 'url': '/admin/main/estante/', 'model_str': 'main.estante', 'icon': 'fas fa-bookmark'}
        )
    if usuario.has_perm('main.change_idioma'):
        side_menu_list[0]['models'].append(
            {'name': 'Idiomas', 'object_name': 'Idiomas', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/idioma/', 'add_url': '/admin/main/idioma/add/', 'view_only': False, 'url': '/admin/main/idioma/', 'model_str': 'main.idioma', 'icon': 'fas fa-language'}
        )
    if usuario.has_perm('main.change_livro'):
        side_menu_list[0]['models'].append(
            {'name': 'Livros', 'object_name': 'Livros', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/livro/', 'add_url': '/admin/main/livro/add/', 'view_only': False, 'url': '/admin/main/livro/', 'model_str': 'main.livro', 'icon': 'fas fa-book'}
        )
    if usuario.is_superuser:
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
                        'icon': 'fas fa-user'
                    },
                ], 'icon': 'fas fa-users-cog'
        }
        )
    return side_menu_list


def links_no_admin(objeto, pode_visualizar, pode_editar):
    links=""
    if pode_visualizar:
        links = links + "<a class='text-reset text-decoration-none' href='{}' title='Visualizar'>{}</a>".format(objeto.get_absolute_url(), bs_icon('info-square'))
    if pode_editar:
        links = links + "<a class='text-reset text-decoration-none' href='{}' title='Editar'>{}</a>".format(objeto.get_edit_url(), bs_icon('pencil-square'))
    return mark_safe(links)