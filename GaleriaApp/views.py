from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Arte, Categoria, Usuario

# Create your views here.

# Usuario --------------------------------------------------------------------------
git 
    
class UsuarioCreateView(CreateView):
    model = Usuario
    fields = ['email', 'idade', 'password']  
    template_name = 'paginas/usuario_form.html'
    success_url = reverse_lazy('login')  # redireciona pro login após cadastro

    def form_valid(self, form):
        # salvar a senha de forma segura (hash)
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        return super().form_valid(form)

# Admin ----------------------------------------------------------------------------
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