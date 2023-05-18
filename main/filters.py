from django.contrib.admin import SimpleListFilter
from django_middleware_global_request import get_request


class LidosFilter(SimpleListFilter):
    title = "Status de Leitura"  # a label for our filter
    parameter_name = "teste"

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            ("lido", "Lido por mim"),
            ("nao_lido", "Não lido por mim"),
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        user = get_request().user
        livros_lidos = user.leitura_set.all().values_list('livro_id', flat=True)
        if self.value() == "lido":
            # Get websites that have at least one page.
            return queryset.distinct().filter(id__in=livros_lidos)
        elif self.value() == "nao_lido":
            # Get websites that don't have any pages.
            return queryset.distinct().exclude(id__in=livros_lidos)