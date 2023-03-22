from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    contato = models.CharField("Contato", max_length=100)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name()

    def get_edit_url(self):
        return '/admin/main/usuario/{}/change/'.format(self.id)