from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email=None, fullname=None, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        if not fullname:
            raise ValueError('O nome completo é obrigatório.')

        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, fullname, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):  # <- muda aqui
    fullname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def save(self, *args, **kwargs):
        # Criptografa a senha se ela ainda não estiver criptografada
        if self.pk is None:  # novo usuário
            self.set_password(self.password)
        else:
            old = Usuario.objects.filter(pk=self.pk).first()
            if old and old.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname