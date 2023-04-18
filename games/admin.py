from django.contrib import admin

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
    list_display = ('get_links', 'titulo', 'tipo', 'genero', 'get_lojas', 'get_plataformas')
    search_fields = ('titulo', )
    list_filter = (
        ('genero', admin.RelatedOnlyFieldListFilter),
        ('lojas', admin.RelatedOnlyFieldListFilter),
        ('plataformas', admin.RelatedOnlyFieldListFilter),
        'tipo',
    )
    list_display_links = None

    def get_lojas(self, obj):
        return obj.lista_lojas()
    get_lojas.short_description = 'Lojas'

    def get_plataformas(self, obj):
        return obj.lista_plataformas()
    get_plataformas.short_description = 'Plataformas'

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
