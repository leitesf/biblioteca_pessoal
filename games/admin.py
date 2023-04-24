from django.contrib import admin
from django.utils.safestring import mark_safe

from games.models import Plataforma, Loja, Genero, Jogo
from main.admin import AdminBasico


class PlataformaAdmin(AdminBasico):
    list_display = ('get_links', 'nome')
    search_fields = ('nome', )
    list_display_links = None


class LojaAdmin(AdminBasico):
    list_display = ('get_links', 'nome')
    search_fields = ('nome', )
    list_display_links = None


class GeneroAdmin(AdminBasico):
    list_display = ('get_links', 'descricao')
    search_fields = ('descricao', )
    list_display_links = None


class JogoAdmin(AdminBasico):
    list_display = ('get_links', 'titulo', 'tipo', 'genero', 'get_plataformas', 'get_lojas', 'possui_capa')
    search_fields = ('titulo', )
    list_filter = (
        ('genero', admin.RelatedOnlyFieldListFilter),
        ('lojas', admin.RelatedOnlyFieldListFilter),
        ('plataformas', admin.RelatedOnlyFieldListFilter),
        'tipo',
        ('capa', admin.EmptyFieldListFilter)
    )
    list_display_links = None

    def get_lojas(self, obj):
        return obj.lista_lojas()
    get_lojas.short_description = 'Lojas'

    def get_plataformas(self, obj):
        return obj.lista_plataformas()
    get_plataformas.short_description = 'Plataformas'

    def possui_capa(self, obj):
        return mark_safe('<span class="badge badge-success">Sim</span>' if obj.capa else '<span class="badge badge-danger">Não</span>')
    possui_capa.short_description = 'Possui capa'

    # def get_actions(self, request):
    #     categorias = dict(
    #         create_action_de_categoria(categoria) for categoria in Categoria.objects.exclude(descricao="A definir")
    #     )
    #     estantes = dict(
    #         create_action_de_estante(estante) for estante in Estante.objects.exclude(descricao="A definir")
    #     )
    #     categorias.update(estantes)
    #     return categorias


admin.site.register(Plataforma, PlataformaAdmin)
admin.site.register(Loja, LojaAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Jogo, JogoAdmin)

# Register your models here.
# Register your models here.
