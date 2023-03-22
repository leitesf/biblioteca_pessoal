from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

#
def gerar_menu(usuario):
    side_menu_list = [
        {
            'name': 'Biblioteca',
            'app_label': 'main',
            'app_url': '/admin/main/',
            'has_module_perms': True,
            'models': []
        }
    ]
    # if usuario.has_perm('main.view_cliente'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Clientes', 'object_name': 'Cliente', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/cliente/', 'add_url': '/admin/main/cliente/add/', 'view_only': False, 'url': '/admin/main/cliente/', 'model_str': 'main.cliente', 'icon': 'fas fa-user-tag'}
    #     )
    # if usuario.has_perm('main.view_notafiscal'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Notas Fiscais', 'object_name': 'Nota Fiscal', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/notafiscal/', 'add_url': '/admin/main/notafiscal/add/', 'view_only': False, 'url': '/admin/main/notafiscal/', 'model_str': 'main.notafiscal', 'icon': 'fas fa-receipt'}
    #     )
    # if usuario.has_perm('main.view_transportador'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Transportadores', 'object_name': 'Transportador', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/transportador/', 'add_url': '/admin/main/transportador/add/', 'view_only': False, 'url': '/admin/main/transportador/', 'model_str': 'main.transportador', 'icon': 'fas fa-truck'}
    #     )
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