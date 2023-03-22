from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from isbn_field import ISBNField


class Usuario(AbstractUser):
    contato = models.CharField("Contato", max_length=100)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name()

    def get_edit_url(self):
        return '/admin/main/usuario/{}/change/'.format(self.id)


class Estante(models.Model):
    descricao = models.CharField("Descrição", max_length=20)
    comodo = models.CharField("Cômodo", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Estante'
        verbose_name_plural = 'Estantes'

    def __str__(self):
        return self.descricao

    def get_edit_url(self):
        return '/admin/main/estante/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/estante/{}/'.format(self.id)


class Categoria(models.Model):
    descricao = models.CharField("Descrição", max_length=20)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.descricao

    def get_edit_url(self):
        return '/admin/main/categoria/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/categoria/{}/'.format(self.id)


class Editora(models.Model):
    nome = models.CharField("Nome", max_length=20)

    class Meta:
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/editora/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/editora/{}/'.format(self.id)


class Idioma(models.Model):
    nome = models.CharField("Nome", max_length=20)

    class Meta:
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'

    def __str__(self):
        return self.nome

    def get_edit_url(self):
        return '/admin/main/idioma/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/idioma/{}/'.format(self.id)


class Autor(models.Model):
    nome = models.CharField("Descrição", max_length=20)
    nacionalidade = CountryField(verbose_name="Nacionalidade")
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

    def __str__(self):
        if self.pseudonimo_de:
            return '{} ({})'.format(self.nome, self.pseudonimo_de)
        else:
            return self.nome

    def get_edit_url(self):
        return '/admin/main/autor/{}/change/'.format(self.id)

    def get_absolute_url(self):
        return '/autor/{}/'.format(self.id)


class Livro(models.Model):
    titulo = models.CharField("Titulo", max_length=20)
    autores = models.ManyToManyField(Autor, verbose_name="Autores")
    isbn = ISBNField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT, verbose_name="Categoria")
    editora = models.ForeignKey(Editora, on_delete=models.RESTRICT, verbose_name="Editora")
    estante = models.ForeignKey(Estante, on_delete=models.RESTRICT, verbose_name="Estante")
    idioma = models.ForeignKey(Idioma, on_delete=models.RESTRICT, verbose_name="Idioma")

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def __str__(self):
        return '{} ({})'.format(self.titulo, self.autores.all())

    def get_edit_url(self):
        return '/admin/main/livro/{}/change/'.format(self.id)

    def lista_autores(self):
        return " / ".join([item.nome for item in self.autores.all()])

    def get_absolute_url(self):
        return '/livro/{}/'.format(self.id)
