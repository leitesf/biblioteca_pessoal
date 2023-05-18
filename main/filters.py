from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django_middleware_global_request import get_request

from main.models import Autor


class LidosFilter(SimpleListFilter):
    title = "Status de Leitura"  # a label for our filter
    parameter_name = "teste"

    def lookups(self, request, model_admin):
        return [
            ("lido", "Lido por mim"),
            ("nao_lido", "Não lido por mim"),
        ]

    def queryset(self, request, queryset):
        user = get_request().user
        livros_lidos = user.leitura_set.all().values_list('livro_id', flat=True)
        if self.value() == "lido":
            return queryset.distinct().filter(id__in=livros_lidos)
        elif self.value() == "nao_lido":
            return queryset.distinct().exclude(id__in=livros_lidos)
        else:
            return queryset


class AutoresFilter(SimpleListFilter):
    title = "Autor"  # a label for our filter
    parameter_name = "teste"

    def lookups(self, request, model_admin):
        return Autor.objects.filter(Q(livros_como_principal__isnull=False) | Q(livros_como_secundario__isnull=False)).\
            distinct().values_list('id', 'nome')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(Q(autor_principal__id=self.value()) | Q(autores_secundarios__id=self.value()))
        else:
            return queryset
