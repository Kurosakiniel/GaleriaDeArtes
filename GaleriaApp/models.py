from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db import models

# Create your models here.
class UsuarioManager(BaseUserManager,):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_active', True)

            if extra_fields.get('is_staff') is not True:
                raise ValueError('O superusuário deve ter is_staff=True')
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('O superusuário deve ter is_superuser=True')

            return self.create_user(email, password, **extra_fields)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)  # opcional
    idade = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'   # login pelo email
    REQUIRED_FIELDS = []       # não precisa de outros campos obrigatórios

    def __str__(self):
        # se o username estiver definido, mostra ele, senão mostra email
        return self.username if self.username else self.email

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Arte(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=50, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    imagem = models.ImageField(upload_to='media/artes', blank=True, null=True)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Entregue', 'Entregue'),
    )

    cliente = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pedidos')
    artes = models.ManyToManyField(Arte, blank=True)  # várias artes por pedido
    data_criacao = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente} - {self.status}'

    def calcular_total(self):
        return sum(arte.preco for arte in self.artes.all())