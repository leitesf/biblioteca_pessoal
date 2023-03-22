from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from main.models import Autor
from main.utils import gerar_menu


@login_required
def show_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    side_menu_list = gerar_menu(request.user)

    pode_gerar_orcamento = request.user.has_perm('main.gerar_orcamento')
    return render(request, 'autor.html', locals())

# Create your views here.
