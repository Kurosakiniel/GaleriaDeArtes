from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.db import models

# Create your models here.
class Usuario(AbstractBaseUser):
    #colocando idade como um adicional
    idade = models.PositiveIntegerField(null=True, blank=True)

    #nao dar caquinha
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username

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

    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    artes = models.ManyToManyField(Arte, blank=True)  # várias artes por pedido
    data_criacao = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente} - {self.status}'

    def calcular_total(self):
        return sum(arte.preco for arte in self.artes.all())