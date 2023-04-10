from django.contrib import admin
from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon
from solo.admin import SingletonModelAdmin

from main.forms import UsuarioForm
from main.models import Usuario, Estante, Categoria, Autor, Idioma, Editora, Livro, Colecao, ConfiguracaoSistema
from django.templatetags.static import static


class AdminBasico(admin.ModelAdmin):
    def get_links(self, obj):
        info = static('svg/info-square.svg')
        pencil = static('svg/pencil-square.svg')
        return mark_safe(
            "<a href='{}' title='Visualizar'><img src='{}'></a>&nbsp;<a href='{}' title='Editar'><img src='{}'></a>".format(obj.get_absolute_url(), info, obj.get_edit_url(), pencil)
        )

    get_links.short_description = '#'
    get_links.allow_tags = True
    list_per_page = 50

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'get_nome', 'username', 'email', 'contato', 'get_grupos', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = None
    form = UsuarioForm

    def get_nome(self, obj):
        return obj.get_full_name()

    get_nome.short_description = 'Nome'
    get_nome.admin_order_field = ["first_name"]

    def get_grupos(self, obj):
        return ', '.join(obj.groups.values_list('name', flat=True))

    get_grupos.short_description = 'Grupos'

    def get_links(self, obj):
        key = static('svg/key.svg')
        pencil = static('svg/pencil-square.svg')
        info = static('svg/info-square.svg')
        links = ""
        links += "<a class='text-reset text-decoration-none' href='{}' title='Visualizar'><img src='{}'></a>".format(obj.get_absolute_url(), info)
        links += "<a class='text-reset text-decoration-none' href='{}' title='Editar'><img src='{}'></a>".format(obj.get_edit_url(), pencil)
        links += "<a class='text-reset text-decoration-none' href='{}' title='Alterar Senha'><img src='{}'></a>".format('/usuario/{}/alterar_senha/'.format(obj.id), key)
        return mark_safe(links)

    get_links.short_description = '#'
    get_links.allow_tags = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class EstanteAdmin(AdminBasico):
    list_display = ('get_links', 'descricao', 'comodo')
    search_fields = ('descricao', 'comodo')
    list_display_links = None


class CategoriaAdmin(AdminBasico):
    list_display = ('get_links', 'descricao', )
    search_fields = ('descricao', )
    list_display_links = None


class EditoraAdmin(AdminBasico):
    list_display = ('get_links', 'nome', )
    search_fields = ('nome', )
    list_display_links = None


class IdiomaAdmin(AdminBasico):
    list_display = ('get_links', 'nome', )
    search_fields = ('nome', )
    list_display_links = None


class ColecaoAdmin(AdminBasico):
    list_display = ('get_links', 'descricao', 'nome_para_ordenacao', 'prioridade_na_ordenacao')
    search_fields = ('descricao', )
    list_filter = (
        ('prioridade_na_ordenacao',)
    )
    list_display_links = None


class AutorAdmin(AdminBasico):
    list_display = ('get_links', 'nome', 'nome_ordenado', 'nacionalidade', 'pseudonimo_de')
    search_fields = ('nome', 'pseudonimo_de', )
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


class LivroAdmin(AdminBasico):
    list_display = ('get_links', 'titulo', 'autor_principal', 'lista_autores', 'editora', 'categoria',  'estante')
    search_fields = ('titulo', 'isbn', )
    list_filter = (
        ('autor_principal', admin.RelatedOnlyFieldListFilter),
        ('autores_secundarios', admin.RelatedOnlyFieldListFilter),
        ('editora', admin.RelatedOnlyFieldListFilter),
        ('categoria', admin.RelatedOnlyFieldListFilter),
        ('estante', admin.RelatedOnlyFieldListFilter),
    )
    list_display_links = None

    def lista_autores(self, obj):
        return obj.lista_autores_secundarios()
    lista_autores.short_description = 'Autores Secundários'

    def get_actions(self, request):
        categorias = dict(
            create_action_de_categoria(categoria) for categoria in Categoria.objects.exclude(descricao="A definir")
        )
        estantes = dict(
            create_action_de_estante(estante) for estante in Estante.objects.exclude(descricao="A definir")
        )
        categorias.update(estantes)
        return categorias


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Estante, EstanteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Editora, EditoraAdmin)
admin.site.register(Idioma, IdiomaAdmin)
admin.site.register(Colecao, ColecaoAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Livro, LivroAdmin)
admin.site.register(ConfiguracaoSistema, SingletonModelAdmin)
# admin.site.index_template = "index.html"
