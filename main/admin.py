from django.contrib import admin
from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

from main.forms import UsuarioForm
from main.models import Usuario, Estante, Categoria, Autor, Idioma, Editora, Livro


class AdminBasico(admin.ModelAdmin):
    def get_links(self, obj):
        links = ""
        links += "<a class='text-reset text-decoration-none' href='{}' title='Visualizar'>{}</a>".format(obj.get_absolute_url(), bs_icon('info-square'))
        links += "<a class='text-reset text-decoration-none' href='{}' title='Editar'>{}</a>".format(obj.get_edit_url(), bs_icon('pencil-square'))
        return mark_safe(links)

    get_links.short_description = '#'
    get_links.allow_tags = True

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
        links = ""
        links += "<a class='text-reset text-decoration-none' href='{}' title='Editar'>{}</a>".format(obj.get_edit_url(), bs_icon('pencil-square'))
        links += "<a class='text-reset text-decoration-none' href='{}' title='Alterar Senha'>{}</a>".format('/usuario/{}/alterar_senha/'.format(obj.id), bs_icon('key'))
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
    list_display = ('get_links', 'descricao')
    search_fields = ('descricao', )
    list_display_links = None


class EditoraAdmin(AdminBasico):
    list_display = ('get_links', 'nome')
    search_fields = ('nome', )
    list_display_links = None


class IdiomaAdmin(AdminBasico):
    list_display = ('get_links', 'nome')
    search_fields = ('nome', )
    list_display_links = None


class AutorAdmin(AdminBasico):
    list_display = ('get_links', 'nome', 'nacionalidade', 'pseudonimo_de')
    search_fields = ('nome', 'pseudonimo_de', )
    list_filter = (
        ('nacionalidade',)
    )
    list_display_links = None


class LivroAdmin(AdminBasico):
    list_display = ('get_links', 'titulo', 'lista_autores', 'editora', 'categoria',  'estante')
    search_fields = ('nome', 'isbn', )
    list_filter = (
        ('autores', admin.RelatedOnlyFieldListFilter),
        ('editora', admin.RelatedOnlyFieldListFilter),
        ('categoria', admin.RelatedOnlyFieldListFilter),
        ('estante', admin.RelatedOnlyFieldListFilter),
    )
    list_display_links = None

    def lista_autores(self, obj):
        return " / ".join([item.nome for item in obj.autores.all()])
    lista_autores.short_description = 'Autores'


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Estante, EstanteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Editora, EditoraAdmin)
admin.site.register(Idioma, IdiomaAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Livro, LivroAdmin)
