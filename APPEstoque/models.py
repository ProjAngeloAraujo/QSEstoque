from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Gerenciador customizado
class UsuarioManager(BaseUserManager):
    def create_user(self, email_usuario=None, nome_usuario=None, nome_completo=None, senha=None, **extra_fields):
        if not email_usuario:
            raise ValueError('O email é obrigatório.')
        if not nome_usuario:
            raise ValueError('O nome de usuário é obrigatório.')
        if not nome_completo:
            raise ValueError('O nome completo é obrigatório.')

        email_usuario = self.normalize_email(email_usuario)
        user = self.model(
            email_usuario=email_usuario,
            nome_usuario=nome_usuario,
            nome_completo=nome_completo,
            **extra_fields
        )

        if senha:
            user.set_password(senha)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email_usuario, nome_usuario, nome_completo, senha, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')
        return self.create_user(email_usuario, nome_usuario, nome_completo, senha, **extra_fields)

# Modelo de usuário
class Usuario(AbstractBaseUser, PermissionsMixin):
    email_usuario = models.EmailField(unique=True)
    nome_usuario = models.CharField(max_length=50, unique=True)
    nome_completo = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email_usuario'
    REQUIRED_FIELDS = ['nome_usuario', 'nome_completo']

    def __str__(self):
        return self.nome_usuario