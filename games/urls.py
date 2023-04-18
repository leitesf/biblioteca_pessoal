from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from games import views

app_name = 'games'

urlpatterns = [
    path('genero/<int:genero_id>/', views.show_genero),
    path('plataforma/<int:plataforma_id>/', views.show_plataforma),
    path('loja/<int:loja_id>/', views.show_loja),
    path('jogo/<int:jogo_id>/', views.show_jogo),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
