from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

#
def gerar_menu(usuario):
    side_menu_list = [
        {
            'name': 'Morro Azul',
            'app_label': 'main',
            'app_url': '/admin/main/',
            'has_module_perms': True,
            'models': []
        }
    ]
    if usuario.has_perm('main.view_cliente'):
        side_menu_list[0]['models'].append(
            {'name': 'Clientes', 'object_name': 'Cliente', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/cliente/', 'add_url': '/admin/main/cliente/add/', 'view_only': False, 'url': '/admin/main/cliente/', 'model_str': 'main.cliente', 'icon': 'fas fa-user-tag'}
        )
    if usuario.has_perm('main.view_notafiscal'):
        side_menu_list[0]['models'].append(
            {'name': 'Notas Fiscais', 'object_name': 'Nota Fiscal', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/notafiscal/', 'add_url': '/admin/main/notafiscal/add/', 'view_only': False, 'url': '/admin/main/notafiscal/', 'model_str': 'main.notafiscal', 'icon': 'fas fa-receipt'}
        )
    if usuario.has_perm('main.view_transportador'):
        side_menu_list[0]['models'].append(
            {'name': 'Transportadores', 'object_name': 'Transportador', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/transportador/', 'add_url': '/admin/main/transportador/add/', 'view_only': False, 'url': '/admin/main/transportador/', 'model_str': 'main.transportador', 'icon': 'fas fa-truck'}
        )
    # if usuario.has_perm('main.view_configuracaopercentualcorretor'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Configurações de Percentual do Corretor', 'object_name': 'ConfiguracaoPercentualCorretor', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/configuracaopercentualcorretor/', 'add_url': '/admin/main/configuracaopercentualcorretor/add/', 'view_only': False, 'url': '/admin/main/configuracaopercentualcorretor/', 'model_str': 'main.configuracaopercentualcorretor', 'icon': 'fas fa-percentage'}
    #     )
    # if usuario.has_perm('main.view_configuracaoprecoregularizacao'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Configurações de Preço de Regularização', 'object_name': 'ConfiguracaoPrecoRegularizacao', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/configuracaoprecoregularizacao/', 'add_url': '/admin/main/configuracaoprecoregularizacao/add/', 'view_only': False, 'url': '/admin/main/configuracaoprecoregularizacao/', 'model_str': 'main.configuracaoprecoregularizacao', 'icon': 'fas fa-money-bill'}
    #     )
    # if usuario.has_perm('main.view_configuracaovalortecnico'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Configurações de Valor do Técnico', 'object_name': 'ConfiguracaoValorTecnico', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/configuracaovalortecnico/', 'add_url': '/admin/main/configuracaovalortecnico/add/', 'view_only': False, 'url': '/admin/main/configuracaovalortecnico/', 'model_str': 'main.configuracaovalortecnico', 'icon': 'fas fa-dollar-sign'}
    #     )
    # if usuario.has_perm('main.view_imovel'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Imóveis', 'object_name': 'Imovel', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/imovel/', 'add_url': '/admin/main/imovel/add/', 'view_only': False, 'url': '/admin/main/imovel/', 'model_str': 'main.imovel', 'icon': 'fas fa-building'}
    #     )
    # if usuario.has_perm('main.view_ordemservico'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Ordens de Serviço', 'object_name': 'OrdemServico', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/ordemservico/', 'add_url': '/admin/main/ordemservico/add/', 'view_only': False, 'url': '/admin/main/ordemservico/', 'model_str': 'main.ordemservico', 'icon': 'fas fa-receipt'}
    #     )
    # if usuario.has_perm('main.view_tiporegularizacao'):
    #     side_menu_list[0]['models'].append(
    #         {'name': 'Tipos de Regularização', 'object_name': 'TipoRegularizacao', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/main/tiporegularizacao/', 'add_url': '/admin/main/tiporegularizacao/add/', 'view_only': False, 'url': '/admin/main/tiporegularizacao/', 'model_str': 'main.tiporegularizacao', 'icon': 'fas fa-tags'}
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
                    {
                        'name': 'Configuração de Pontuação',
                        'url': '/admin/main/configuracaopontuacao/',
                        'children': None,
                        'new_window': False,
                        'icon': 'fas fa-tools'
                    }
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