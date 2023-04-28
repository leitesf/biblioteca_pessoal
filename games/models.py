from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class Plataforma(models.Model):
    nome = models.CharField("Nome", max_length=50, unique=True)

    class Meta:
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/games/plataforma/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/plataforma/{}/'.format(self.id)


class Loja(models.Model):
    nome = models.CharField("Nome", max_length=50, unique=True)

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/games/loja/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/loja/{}/'.format(self.id)


class Franquia(models.Model):
    nome = models.CharField("Nome", max_length=50, unique=True)
    filha_de = models.ForeignKey(
        'games.Franquia', on_delete=models.RESTRICT, verbose_name="Filha de", null=True, blank=True,
        related_name='filhas'
    )

    class Meta:
        verbose_name = 'Franquia'
        verbose_name_plural = 'Franquias'
        ordering = ['nome']

    def __str__(self):
        if self.filha_de:
            return '{} ({})'.format(self.nome, self.filha_de.nome)
        else:
            return self.nome

    def get_edit_url(self):
        return '/admin/games/franquia/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/franquia/{}/'.format(self.id)


class Genero(models.Model):
    descricao = models.CharField("Descrição", max_length=50, unique=True)

    class Meta:
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao

    def get_edit_url(self):
        return '/admin/games/genero/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/genero/{}/'.format(self.id)


class TipoJogo:
    FISICO = 'Físico'
    DIGITAL = 'Digital'

    TIPOS = ((FISICO, 'Físico'), (DIGITAL, 'Digital'))

    @classmethod
    def get_status(cls, status):
        for tipo in cls.TIPOS:
            if tipo[0]==status:
                return tipo[1]


class Jogo(models.Model):
    titulo = models.CharField("Titulo", max_length=100)
    tipo = models.CharField("Tipo", choices=TipoJogo.TIPOS, max_length=7, default=TipoJogo.DIGITAL)
    genero = models.ForeignKey(Genero, on_delete=models.RESTRICT, verbose_name="Gênero", null=True, blank=True)
    lojas = models.ManyToManyField(Loja, verbose_name="Lojas", related_name='jogos', blank=True)
    plataformas = models.ManyToManyField(
        Plataforma, verbose_name="Plataformas", related_name='jogos', blank=True
    )
    franquias = models.ManyToManyField(
        Franquia, verbose_name="Franquias", related_name='jogos', blank=True
    )
    steam_id = models.IntegerField('ID no Steam', blank=True, null=True, unique=True)
    nao_existe_no_steam = models.BooleanField(
        verbose_name="Não existe no steam",
        help_text="Marque esse campo para evitar que se realize a busca no steam desse título",
        default=False
    )
    capa = models.ImageField("Capa do Jogo", upload_to="capas_jogo", null=True, blank=True)

    class Meta:
        verbose_name = 'Jogo'
        verbose_name_plural = 'Jogos'
        ordering = ['titulo']
        unique_together = ['titulo', 'tipo']

    def __str__(self):
        return self.titulo

    def get_edit_url(self):
        return '/admin/games/jogo/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/jogo/{}/'.format(self.id)

    def lista_lojas(self):
        return " / ".join([item.nome for item in self.lojas.all()])

    def lista_franquias(self):
        return " / ".join([item.nome for item in self.franquias.all()])

    def lista_plataformas(self):
        return " / ".join([item.nome for item in self.plataformas.all()])

    @classmethod
    def limpar_capas_defeituosas(cls):
        jogos = []
        for jogo in cls.objects.exclude(capa__exact=''):
            if jogo.capa.size == 146:
                jogo.capa = None
                jogo.save()
                jogos.append(jogo.titulo)
        print(', '.join(jogos))


@receiver(post_save, sender=Jogo)
def importar_capa_e_genero(sender, instance, **kwargs):
    from games.importador import ImportadorSteamFront
    importador = ImportadorSteamFront()
    if instance.steam_id and not instance.capa:
        importador.atualizar_capa_de_jogo(instance)
    if instance.steam_id and not instance.genero:
        importador.atualizar_genero_de_jogo(instance)
