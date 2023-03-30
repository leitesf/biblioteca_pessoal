from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from main.forms import LeituraForm
from main.models import Autor, Livro, Categoria, Editora, Idioma, Estante, Colecao, Leitura
from main.utils import gerar_menu


def index(request):
    return redirect('/admin/')

@login_required
def show_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    side_menu_list = gerar_menu(request.user, 'autor')
    return render(request, 'autor.html', locals())


@login_required
def show_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    side_menu_list = gerar_menu(request.user, 'livro')
    ja_li = livro.leitura_set.filter(usuario=request.user).exists()
    pode_registrar_leitura = request.user.has_perm('main.add_leitura')
    return render(request, 'livro.html', locals())


@login_required
def show_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    side_menu_list = gerar_menu(request.user, 'categoria')
    return render(request, 'categoria.html', locals())


@login_required
def show_editora(request, editora_id):
    editora = get_object_or_404(Editora, id=editora_id)
    side_menu_list = gerar_menu(request.user, 'editora')
    return render(request, 'editora.html', locals())


@login_required
def show_colecao(request, colecao_id):
    colecao = get_object_or_404(Colecao, id=colecao_id)
    side_menu_list = gerar_menu(request.user, 'colecao')
    return render(request, 'colecao.html', locals())


@login_required
def show_idioma(request, idioma_id):
    idioma = get_object_or_404(Idioma, id=idioma_id)
    side_menu_list = gerar_menu(request.user, 'idioma')
    return render(request, 'idioma.html', locals())


@login_required
def show_estante(request, estante_id):
    estante = get_object_or_404(Estante, id=estante_id)
    side_menu_list = gerar_menu(request.user, 'estante')
    return render(request, 'estante.html', locals())


@permission_required('main.add_leitura')
def form_leitura(request, leitura_id=None, livro_id=None):
    side_menu_list = gerar_menu(request.user, ativo='livro')
    if leitura_id:
        leitura = get_object_or_404(Leitura, id=leitura_id)
    else:
        leitura = Leitura()
        leitura.usuario = request.user
        leitura.livro = get_object_or_404(Livro, id=livro_id)
    titulo = "Registrar Leitura de Livro"

    if request.method == "POST":
        form = LeituraForm(request.POST, instance=leitura)
        if form.is_valid():
            leitura.save()
            messages.success(request, 'Leitura registrada com sucesso.')
            return redirect(leitura.livro.get_absolute_url(), )
    else:
        form = LeituraForm(instance=leitura, user=request.user)
    return render(request, 'form.html', locals())


@permission_required('main.add_leitura')
def excluir_leitura(request, leitura_id=None):
    side_menu_list = gerar_menu(request.user, ativo='livro')
    leitura = get_object_or_404(Leitura, id=leitura_id)
    livro = leitura.livro
    if leitura.usuario != request.user:
        messages.error(request, 'Você não pode efetuar a exclusão de uma leitura que não for sua.')
        return redirect(livro.get_absolute_url(), )
    if leitura.delete():
        messages.success(request, 'Leitura removida com sucesso.')
        return redirect(livro.get_absolute_url(), )

# Create your views here.
