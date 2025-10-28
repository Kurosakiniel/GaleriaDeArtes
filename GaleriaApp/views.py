from django.shortcuts import render
from django.views.generic import ListView
from .models import Arte
from .models import Arte, Categoria

# Create your views here.
class ArteListView(ListView):
    model = Arte
    template_name = 'paginas/arte_list.html'  
    context_object_name = 'artes'  

    def get_queryset(self):
        qs = super().get_queryset()
        categoria_nome = self.request.GET.get('categoria')  
        if categoria_nome:
            qs = qs.filter(categoria__nome__iexact=categoria_nome)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  
        return context