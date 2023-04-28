from django.core.management.base import BaseCommand

from games.models import Jogo


class Command(BaseCommand):
    help = "Limpa capas defeituosas de jogos"

    def handle(self, *args, **options):
        Jogo.limpar_capas_defeituosas()
