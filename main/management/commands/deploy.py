from django.core.management import call_command
from django.core.management.base import BaseCommand

from main.models import ConfiguracaoSistema


class Command(BaseCommand):
    help = "Realiza os passos necessários para executar o deploy"

    def handle(self, *args, **options):
        call_command('migrate')
        call_command('loaddata', 'main/fixtures/grupos.json')
        call_command('loaddata', 'games/fixtures/cadastros.json')
        configuracao = ConfiguracaoSistema.objects.first()
        if configuracao and configuracao.usuario_principal and configuracao.usuario_principal.skoob_user:
            call_command('importar_skoob')
        if configuracao and configuracao.usuario_principal and configuracao.usuario_principal.steam_user and \
                configuracao.steam_api_key:
            call_command('importar_steam')
