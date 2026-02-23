from django.contrib import admin
from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon
from solo.admin import SingletonModelAdmin

from main.filters import LidosFilter, AutoresFilter
from main.forms import UsuarioForm
from main.models import Usuario, Estante, Categoria, Autor, Idioma, Editora, Livro, Colecao, ConfiguracaoSistema, \
    Emprestimo
from django.templatetags.static import static
from django_middleware_global_request import get_request

from main.utils import get_badge_boolean


class AdminBasico(admin.ModelAdmin):
    @admin.display(
        description='#'
    )
    def get_links(self, obj):
        info = static('svg/info-square.svg')
        pencil = static('svg/pencil-square.svg')
        return mark_safe(
            "<a href='{}' title='Visualizar'><img src='{}'></a>&nbsp;<a href='{}' title='Editar'><img src='{}'></a>".format(obj.get_absolute_url(), info, obj.get_edit_url(), pencil)
        )

    list_per_page = 50

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'get_nome', 'username', 'email', 'contato', 'get_grupos', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = None
    form = UsuarioForm

    @admin.display(
        description='Nome',
        ordering=["first_name"],
    )
    def get_nome(self, obj):
        return obj.get_full_name()


    @admin.display(
        description='Grupos'
    )
    def get_grupos(self, obj):
        return ', '.join(obj.groups.values_list('name', flat=True))


    @admin.display(
        description='#'
    )
    def get_links(self, obj):
        key = static('svg/key.svg')
        pencil = static('svg/pencil-square.svg')
        info = static('svg/info-square.svg')
        links = ""
        links += "<a class='text-reset text-decoration-none' href='{}' title='Visualizar'><img src='{}'></a>".format(obj.get_absolute_url(), info)
        links += "<a class='text-reset text-decoration-none' href='{}' title='Editar'><img src='{}'></a>".format(obj.get_edit_url(), pencil)
        links += "<a class='text-reset text-decoration-none' href='{}' title='Alterar Senha'><img src='{}'></a>".format('/usuario/{}/alterar_senha/'.format(obj.id), key)
        return mark_safe(links)


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Estante)
class EstanteAdmin(AdminBasico):
    list_display = ('get_links', 'descricao', 'comodo')
    search_fields = ('descricao', 'comodo')
    list_display_links = None


@admin.register(Categoria)
class CategoriaAdmin(AdminBasico):
    list_display = ('get_links', 'descricao', )
    search_fields = ('descricao', )
    list_display_links = None


@admin.register(Editora)
class EditoraAdmin(AdminBasico):
    list_display = ('get_links', 'nome', )
    search_fields = ('nome', )
    list_display_links = None


@admin.register(Idioma)
class IdiomaAdmin(AdminBasico):
    list_display = ('get_links', 'nome', )
    search_fields = ('nome', )
    list_display_links = None


@admin.register(Colecao)
class ColecaoAdmin(AdminBasico):
    list_display = ('get_links', 'descricao', 'nome_para_ordenacao', 'prioridade_na_ordenacao')
    search_fields = ('descricao', )
    list_filter = (
        ('prioridade_na_ordenacao',)
    )
    list_display_links = None


@admin.register(Autor)
class AutorAdmin(AdminBasico):
    list_display = ('get_links', 'nome', 'nome_ordenado', 'nacionalidade', 'pseudonimo_de')
    exclude = ['nome_ordenado']
    search_fields = ('nome', 'pseudonimo_de__nome', )
    list_filter = (
        ('nacionalidade',)
    )
    list_display_links = None


def create_action_de_categoria(categoria):
    def action(modeladmin, request, queryset): queryset.update(categoria=categoria)
    name = "mark_%s" % (categoria,)
    return name, (action, name, "Definir a categoria como %s" % (categoria,))


def create_action_de_estante(estante):
    def action(modeladmin, request, queryset): queryset.update(estante=estante)
    name = "mark_%s" % (estante,)
    return name, (action, name, "Definir a estante como %s" % (estante,))


@admin.register(Livro)
class LivroAdmin(AdminBasico):
    list_display = (
        'get_links', 'titulo', 'lista_autores', 'editora', 'categoria',
        'colecao', 'estante', 'lido_por_mim'
    )
    search_fields = ('titulo', 'isbn', )
    list_filter = (
        AutoresFilter,
        ('editora', admin.RelatedOnlyFieldListFilter),
        ('categoria', admin.RelatedOnlyFieldListFilter),
        ('estante', admin.RelatedOnlyFieldListFilter),
        ('colecao', admin.RelatedOnlyFieldListFilter),
        LidosFilter
    )
    list_display_links = None

    @admin.display(
        description='Autores',
        ordering=['autor_principal'],
    )
    def lista_autores(self, obj):
        return obj.lista_todos_autores()

    @admin.display(
        description='Lido por mim?'
    )
    def lido_por_mim(self, obj):
        return get_badge_boolean(obj.lido_por(get_request().user))

    def get_actions(self, request):
        categorias = dict(
            create_action_de_categoria(categoria) for categoria in Categoria.objects.exclude(descricao="A definir")
        )
        estantes = dict(
            create_action_de_estante(estante) for estante in Estante.objects.exclude(descricao="A definir")
        )
        categorias.update(estantes)
        return categorias

    @admin.display(
        description='#'
    )
    def get_links(self, obj):
        info = static('svg/info-square.svg')
        pencil = static('svg/pencil-square.svg')
        image = static('svg/card-image.svg')
        return mark_safe(
            "<a href='{}' title='Visualizar'><img src='{}'></a>&nbsp;<a href='{}' title='Editar'><img src='{}'>&nbsp;</a><a class='show-capa' href='/livro/{}/capa/' data-popup-url='/livro/{}/capa/'><img src='{}'></a>".format(obj.get_absolute_url(), info, obj.get_edit_url(), pencil, obj.id, obj.id, image)
        )



@admin.register(Emprestimo)
class EmprestimoAdmin(AdminBasico):
    list_display = ('get_links', 'livro', 'pessoa', 'data_inicio', 'data_fim')
    search_fields = ('livro', 'pessoa', )
    list_display_links = None

    @admin.display(
        description='#'
    )
    def get_links(self, obj):
        pencil = static('svg/pencil-square.svg')
        return mark_safe(
            "<a href='{}' title='Editar'><img src='{}'></a>".format(obj.get_edit_url(), pencil)
        )



admin.site.register(ConfiguracaoSistema, SingletonModelAdmin)
# admin.site.index_template = "index.html"
