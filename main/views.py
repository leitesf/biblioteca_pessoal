from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from main.models import Autor, Livro
from main.utils import gerar_menu


@login_required
def show_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    side_menu_list = gerar_menu(request.user)
    return render(request, 'autor.html', locals())


@login_required
def show_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    side_menu_list = gerar_menu(request.user)
    return render(request, 'livro.html', locals())

# Create your views here.
