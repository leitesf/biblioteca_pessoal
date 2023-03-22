from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView
from main import views
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
                  path('autor/<int:autor_id>/', views.show_autor),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
