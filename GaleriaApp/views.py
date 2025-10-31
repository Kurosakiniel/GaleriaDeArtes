from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Arte, Categoria, Usuario
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# Usuario --------------------------------------------------------------------------
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
    
class GaleriaPublicaView(ListView):
    model = Arte
    template_name = 'paginas/arte_publica.html'
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
    
class UsuarioCreateView(CreateView):
    model = Usuario
    fields = ['username', 'email', 'idade', 'password']  
    template_name = 'paginas/usuario_form.html'
    success_url = reverse_lazy('login')  # redireciona pro login após cadastro

    def form_valid(self, form):
        # salvar a senha de forma segura (hash)
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        return super().form_valid(form)


# Admin ----------------------------------------------------------------------------
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

class ArteCreateView(CreateView):
    model = Arte
    fields = ['nome', 'categoria', 'preco', 'imagem', 'descricao']
    template_name = 'paginas/arte_form.html'
    success_url = reverse_lazy('arte_list')

class ArteUpdateView(UpdateView):
    model = Arte
    fields = ['nome', 'categoria', 'preco', 'imagem', 'descricao']
    template_name = 'paginas/arte_form.html'
    success_url = reverse_lazy('arte_list')

class ArteDeleteView(DeleteView):
    model = Arte
    template_name = 'paginas/arte_confirm_delete.html'
    success_url = reverse_lazy('arte_list')