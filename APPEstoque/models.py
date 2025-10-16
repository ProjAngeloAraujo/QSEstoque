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
        if self.pk is None:  # novo usuário
            self.set_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.fullname

class Container(models.Model):
    id_container = models.AutoField(primary_key=True)
    nome_container = models.CharField(max_length=100)
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('desativado', 'Desativado'),
        ('cheio', 'Cheio'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    
    ultimas_alteracoes = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_container} ({self.status})"

class Produto(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='produtos')
    nome_produto = models.CharField(max_length=100)

    GRAMAGEM_CHOICES = [
        ('800gr', '800 GR'),
        ('1kg', '1 KG'),
        ('2kg', '2 KG'),
        ('2.5kg', '2.5 KG'),
        ('5kg', '5 KG'),
    ]
    gramagem_produto = models.CharField(max_length=10, choices=GRAMAGEM_CHOICES)

    STATUS_PRODUTO_CHOICES = [
        ('frito_congelado', 'Frito e Congelado'),
        ('cru_congelado', 'Cru e Congelado'),
    ]
    status_produto = models.CharField(max_length=20, choices=STATUS_PRODUTO_CHOICES)

    quantidade_produto = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nome_produto} ({self.gramagem_produto})"

class Pedido(models.Model):
    numero_cliente_pedido = models.CharField(max_length=20, unique=True)
    nome_cliente_pedido = models.CharField(max_length=100)
    regiao_pedido = models.CharField(max_length=100)

    FALTA_CHOICES = [
        ('sim', 'Sim'),
        ('nao', 'Não'),
    ]
    falta = models.CharField(max_length=3, choices=FALTA_CHOICES, default='nao')

    STATUS_PEDIDO_CHOICES = [
        ('separar', 'Separar'),
        ('separado', 'Separado'),
        ('entregue', 'Entregue'),
    ]
    status_pedido = models.CharField(max_length=20, choices=STATUS_PEDIDO_CHOICES, default='separar')

    data_criacao = models.DateTimeField(auto_now_add=True)
    ultimas_alteracoes = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.numero_cliente_pedido} - {self.nome_cliente_pedido}"