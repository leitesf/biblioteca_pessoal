
from django.core.management.base import BaseCommand

from main.models import Usuario
from main.utils import importar_skoob_usuario


class Command(BaseCommand):
    help = "Converte um arquivo livros.json baixado do skoob em livros cadastrados no sistema"

    def handle(self, *args, **options):
        for usuario in Usuario.objects.filter(skoob_authentication__isnull=False):
            importar_skoob_usuario(usuario)
