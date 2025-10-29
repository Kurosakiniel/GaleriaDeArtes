from django.contrib import admin
from .models import Categoria, Arte, Pedido, Usuario

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Arte)
admin.site.register(Pedido)
admin.site.register(Usuario)