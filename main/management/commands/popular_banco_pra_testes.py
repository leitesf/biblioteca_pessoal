# -*- coding: utf-8 -*-
from django_countries.fields import Country

from main.models import Livro, Autor, Estante, Categoria, Editora, Idioma
from faker import Faker
from random import randint
faker = Faker('pt_BR')

Idioma.objects.create(
    nome='Português'
)
Idioma.objects.create(
    nome='Inglês'
)
Idioma.objects.create(
    nome='Espanhol'
)
Estante.objects.create(
    descricao='Esquerda',
    comodo='Escritório'
)
Estante.objects.create(
    descricao='Direita',
    comodo='Escritório'
)
Categoria.objects.create(
    descricao="Literatura"
)
Categoria.objects.create(
    descricao="História em Quadrinhos"
)
Editora.objects.create(
    nome='Rocco'
)
Editora.objects.create(
    nome='Sextante'
)
Editora.objects.create(
    nome='LP&M'
)
Editora.objects.create(
    nome='Intrínseca'
)
countries = ['BR', 'AR', 'GB', 'US']
for i in range(10):
    Autor.objects.create(
        nome=faker.unique.name(),
        nacionalidade=Country(code=countries[randint(0, 3)])
    )
for i in range(100):
    livro = Livro.objects.create(
        titulo=faker.unique.catch_phrase(),
        isbn=faker.isbn10(),
        categoria=Categoria.objects.all()[randint(0, 1)],
        editora=Editora.objects.all()[randint(0, 3)],
        estante=Estante.objects.all()[randint(0, 1)],
        idioma=Idioma.objects.all()[randint(0, 2)],
    )
    for x in range(2):
        livro.autores.add(Autor.objects.all()[randint(0, 9)])

