from ajax_select import register, LookupChannel
from main.models import Autor


@register('autores')
class AutoresLookup(LookupChannel):
    model = Autor

    def get_query(self, q, request):
        return self.model.objects.filter(nome__icontains=q).order_by('nome')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.nome
