from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index),
    path('autor/<int:autor_id>/', views.show_autor),
    path('mesclar_autores/', views.mesclar_autores),
    path('mesclar_editoras/', views.mesclar_editoras),
    path('livro/<int:livro_id>/', views.show_livro),
    path('livro/<int:livro_id>/capa/', views.show_capa_livro),
    path('categoria/<int:categoria_id>/', views.show_categoria),
    path('colecao/<int:colecao_id>/', views.show_colecao),
    path('editora/<int:editora_id>/', views.show_editora),
    path('idioma/<int:idioma_id>/', views.show_idioma),
    path('usuario/<int:usuario_id>/', views.show_usuario),
    path('meus_livros_lidos/', views.show_usuario),
    path('estante/<int:estante_id>/', views.show_estante),
    path('leitura/<int:livro_id>/registrar/', views.form_leitura),
    path('leitura/<int:leitura_id>/editar/', views.form_leitura),
    path('leitura/<int:leitura_id>/excluir/', views.excluir_leitura),
    path('usuario/<int:usuario_id>/alterar_senha/', views.alterar_senha),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
