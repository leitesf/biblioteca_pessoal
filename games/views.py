from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from games.models import Plataforma, Loja, Genero, Jogo, Franquia
from main.utils import gerar_menu


@login_required
def show_plataforma(request, plataforma_id):
    plataforma = get_object_or_404(Plataforma, id=plataforma_id)
    side_menu_list = gerar_menu(request.user, 'plataforma')
    return render(request, 'plataforma.html', locals())


@login_required
def show_loja(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id)
    side_menu_list = gerar_menu(request.user, 'loja')
    return render(request, 'loja.html', locals())


@login_required
def show_franquia(request, franquia_id):
    franquia = get_object_or_404(Franquia, id=franquia_id)
    side_menu_list = gerar_menu(request.user, 'franquia')
    return render(request, 'franquia.html', locals())


@login_required
def show_genero(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)
    side_menu_list = gerar_menu(request.user, 'genero')
    return render(request, 'genero.html', locals())


@login_required
def show_jogo(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    side_menu_list = gerar_menu(request.user, 'jogo')
    pode_editar = request.user.has_perm('games.edit_jogo')
    return render(request, 'jogo.html', locals())


@login_required
def show_capa_jogo(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    return render(request, 'jogo_capa.html', locals())
