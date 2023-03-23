from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('autor/<int:autor_id>/', views.show_autor),
    path('livro/<int:livro_id>/', views.show_livro),
    path('categoria/<int:categoria_id>/', views.show_categoria),
    path('editora/<int:editora_id>/', views.show_editora),
    path('idioma/<int:idioma_id>/', views.show_idioma),
    path('estante/<int:estante_id>/', views.show_estante),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
