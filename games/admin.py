from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.contrib import messages

from games.models import Plataforma, Loja, Genero, Jogo, Franquia
from main.admin import AdminBasico
from django.templatetags.static import static

from main.utils import get_badge_boolean


class PlataformaAdmin(AdminBasico):
    list_display = ('get_links', 'nome')
    search_fields = ('nome', )
    list_display_links = None


class LojaAdmin(AdminBasico):
    list_display = ('get_links', 'nome')
    search_fields = ('nome', )
    list_display_links = None


class FranquiaAdmin(AdminBasico):
    list_display = ('get_links', 'nome', 'filha_de')
    search_fields = ('nome', )
    list_filter = (
        'filha_de',
    )
    list_display_links = None


class GeneroAdmin(AdminBasico):
    list_display = ('get_links', 'descricao')
    search_fields = ('descricao', )
    list_display_links = None

def create_action_de_franquia(franquia):
    def action(modeladmin, request, queryset):
        for jogo in queryset.all():
            jogo.franquias.add(franquia)
            jogo.save()
    name = "mark_%s" % (franquia,)
    return name, (action, name, "Definir a franquia como %s" % (franquia,))


class JogoAdmin(AdminBasico):
    list_display = ('get_links', 'titulo', 'tipo', 'genero', 'get_franquias', 'get_plataformas', 'get_lojas', 'possui_port', 'steam_id', 'possui_capa')
    search_fields = ('titulo', 'steam_id',)
    list_filter = (
        ('genero', admin.RelatedOnlyFieldListFilter),
        ('franquias', admin.RelatedOnlyFieldListFilter),
        ('lojas', admin.RelatedOnlyFieldListFilter),
        ('plataformas', admin.RelatedOnlyFieldListFilter),
        'tipo',
        ('capa', admin.EmptyFieldListFilter),
        ('possui_port', admin.BooleanFieldListFilter),
        ('steam_id', admin.EmptyFieldListFilter)
    )
    list_display_links = None

    def get_links(self, obj):
        info = static('svg/info-square.svg')
        pencil = static('svg/pencil-square.svg')
        image = static('svg/card-image.svg')
        return mark_safe(
            "<a href='{}' title='Visualizar'><img src='{}'></a>&nbsp;<a href='{}' title='Editar'><img src='{}'>&nbsp;</a><a class='show-capa' href='/jogo/{}/capa/' data-popup-url='/jogo/{}/capa/'><img src='{}'></a>".format(obj.get_absolute_url(), info, obj.get_edit_url(), pencil, obj.id, obj.id, image)
        )

    get_links.short_description = '#'
    get_links.allow_tags = True

    def get_lojas(self, obj):
        return obj.lista_lojas()
    get_lojas.short_description = 'Lojas'

    def get_franquias(self, obj):
        return obj.lista_franquias()
    get_franquias.short_description = 'Franquias'

    def get_plataformas(self, obj):
        return obj.lista_plataformas()
    get_plataformas.short_description = 'Plataformas'

    def possui_capa(self, obj):
        return get_badge_boolean(obj.capa)
    possui_capa.short_description = 'Possui capa?'

    def response_add(self, request, obj, post_url_continue=None):
        if '_continue' in request.POST:
            msg = "O jogo “{}” foi adicionado com sucesso, você pode continuar editando o mesmo.".format(obj.titulo)
            self.message_user(request, msg, messages.SUCCESS)
            return redirect(obj.get_edit_url())
        elif '_addanother' in request.POST:
            msg = "O jogo “{}” foi adicionado com sucesso, você pode adicionar outro abaixo.".format(obj.titulo)
            self.message_user(request, msg, messages.SUCCESS)
            return redirect(reverse('admin:games_jogo_add'))
        else:
            msg = "O jogo “{}” foi adicionado com sucesso.".format(obj.titulo)
            self.message_user(request, msg, messages.SUCCESS)
            return redirect(obj.get_absolute_url())

    def response_change(self, request, obj, post_url_continue=None):
        return redirect(obj.get_absolute_url())

    def get_actions(self, request):
        franquias = dict(
            create_action_de_franquia(franquia) for franquia in Franquia.objects.all()
        )
        return franquias


admin.site.register(Plataforma, PlataformaAdmin)
admin.site.register(Loja, LojaAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Jogo, JogoAdmin)
admin.site.register(Franquia, FranquiaAdmin)
