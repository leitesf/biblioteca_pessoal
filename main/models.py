from datetime import date, timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from isbn_field import ISBNField
from solo.models import SingletonModel


class Usuario(AbstractUser):
    contato = models.CharField("Contato", max_length=100)
    skoob_user = models.IntegerField("Usuário no Skoob", blank=True, null=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name']

    def __str__(self):
        return self.get_full_name()

    def get_edit_url(self):
        return '/admin/main/usuario/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/usuario/{}/'.format(self.id)


class Estante(models.Model):
    descricao = models.CharField("Descrição", max_length=50)
    comodo = models.CharField("Cômodo", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Estante'
        verbose_name_plural = 'Estantes'
        ordering = ['descricao']
        unique_together = ['descricao', 'comodo']

    def __str__(self):
        return self.descricao

    def get_edit_url(self):
        return '/admin/main/estante/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/estante/{}/'.format(self.id)


class Categoria(models.Model):
    descricao = models.CharField("Descrição", max_length=50, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao

    def get_edit_url(self):
        return '/admin/main/categoria/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/categoria/{}/'.format(self.id)


class Editora(models.Model):
    nome = models.CharField("Nome", max_length=50, unique=True)

    class Meta:
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'
        ordering = ['nome']
        permissions = [
            (
                "mesclar_editoras",
                "Pode mesclar editoras"
            )
        ]

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/editora/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/editora/{}/'.format(self.id)


class Idioma(models.Model):
    nome = models.CharField("Nome", max_length=100, unique=True)

    class Meta:
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/idioma/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/idioma/{}/'.format(self.id)


class Colecao(models.Model):
    descricao = models.CharField("Coleção", max_length=50, unique=True)
    nome_para_ordenacao = models.CharField("Nome para Ordenação", max_length=30)
    prioridade_na_ordenacao = models.BooleanField(
        "Prioritário na ordenação",
        default=False,
        help_text="Caso ativado, irá agrupar os livros dessa coleção na ordem da prateleira no lugar do autor."
    )

    class Meta:
        verbose_name = 'Coleção'
        verbose_name_plural = 'Coleções'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao

    def get_edit_url(self):
        return '/admin/main/colecao/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/colecao/{}/'.format(self.id)


class Autor(models.Model):
    nome = models.CharField("Nome", max_length=100, unique=True)
    nome_ordenado = models.CharField("Nome Ordenado", max_length=100)
    nacionalidade = CountryField(verbose_name="Nacionalidade", null=True)
    pseudonimo_de = models.ForeignKey(
        'main.Autor',
        related_name="pseudonimos",
        blank=True,
        null=True,
        on_delete=models.RESTRICT
    )

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nome']
        permissions = [
            (
                "mesclar_autores",
                "Pode mesclar autores"
            )
        ]

    def __str__(self):
        if self.pseudonimo_de:
            return '{} ({})'.format(self.nome, self.pseudonimo_de)
        else:
            return self.nome

    def get_edit_url(self):
        return '/admin/main/autor/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/autor/{}/'.format(self.id)


@receiver(pre_save, sender=Autor)
def atualizar_nome_ordenado(sender, instance, **kwargs):
    nome_dividido = instance.nome.split(' ')
    if len(nome_dividido) > 1:
        instance.nome_ordenado = ' '.join(nome_dividido[-1:] + nome_dividido[:-1])
    else:
        instance.nome_ordenado = instance.nome


class Livro(models.Model):
    titulo = models.CharField("Titulo", max_length=100)
    autor_principal = models.ForeignKey(
        Autor,
        on_delete=models.RESTRICT,
        verbose_name='Autor Principal',
        related_name='livros_como_principal'
    )
    autores_secundarios = models.ManyToManyField(
        Autor,
        verbose_name="Autores Secundários",
        related_name='livros_como_secundario'
    )
    isbn = ISBNField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT, verbose_name="Categoria")
    editora = models.ForeignKey(Editora, on_delete=models.RESTRICT, verbose_name="Editora")
    estante = models.ForeignKey(Estante, on_delete=models.RESTRICT, verbose_name="Estante")
    colecao = models.ForeignKey(Colecao, on_delete=models.SET_NULL, verbose_name="Coleção", null=True, blank=True)
    idioma = models.ForeignKey(Idioma, on_delete=models.RESTRICT, verbose_name="Idioma")
    sinopse = models.TextField(verbose_name="Sinopse", blank=True)
    paginas = models.IntegerField(verbose_name="Páginas", blank=True, null=True)
    subtitulo = models.CharField("Subtítulo", max_length=100, blank=True, null=True)
    ano = models.IntegerField(verbose_name="Ano de Publicação", blank=True, null=True)
    skoob_id = models.IntegerField('ID no Skoob', blank=True, null=True, unique=True)
    capa = models.ImageField("Capa do Livro", upload_to="capas_livro", null=True, blank=True)

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['autor_principal__nome_ordenado', 'titulo']

    def __str__(self):
        return '{} ({})'.format(self.titulo, self.autor_principal)

    def get_edit_url(self):
        return '/admin/main/livro/{}/change/'.format(self.id)

    def lista_autores_secundarios(self):
        return " / ".join([item.nome for item in self.autores_secundarios.all().order_by('id')])

    def lista_todos_autores(self):
        autores = [self.autor_principal.nome]
        for autor in self.autores_secundarios.all():
            autores.append(autor.nome)
        return " / ".join(autores)

    def get_absolute_url(self):
        return '/livro/{}/'.format(self.id)


class Leitura(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data = models.DateField(verbose_name="Data de Leitura")

    class Meta:
        verbose_name = 'Leitura'
        verbose_name_plural = 'Leituras'
        ordering = ['livro__autor_principal__nome_ordenado', 'livro__titulo', 'data']


class ConfiguracaoSistema(SingletonModel):
    usuario_principal = models.ForeignKey(Usuario, on_delete=models.SET_NULL, verbose_name="Usuário Principal", null=True)

    def __str__(self):
        return "Configuração do Sistema"

    class Meta:
        verbose_name = "Configuração do Sistema"
