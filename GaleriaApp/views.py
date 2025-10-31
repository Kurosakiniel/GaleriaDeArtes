from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Arte, Categoria, Usuario, Pedido
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.

# Usuario --------------------------------------------------------------------------   
class GaleriaPublicaView(ListView):
    model = Arte
    template_name = 'galeriaapp/arte_publica.html'
    context_object_name = 'artes'

    def get_queryset(self):
        qs = super().get_queryset()
        categoria_nome = self.request.GET.get('categoria')
        if categoria_nome:
            qs = qs.filter(categoria__nome__iexact=categoria_nome)
        return qs.exclude(id__isnull=True)  # remove qualquer arte sem id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context
    
class UsuarioCreateView(CreateView):
    model = Usuario
    fields = ['username', 'email', 'idade', 'password']  
    template_name = 'galeriaapp/usuario_form.html'
    success_url = reverse_lazy('login')  # redireciona pro login após cadastro

    def form_valid(self, form):
        # salvar a senha de forma segura (hash)
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        return super().form_valid(form)

class AdicionarAoPedidoView(LoginRequiredMixin, View):
    def post(self, request, arte_id):
        arte = get_object_or_404(Arte, id=arte_id)
        usuario = request.user

        # Cria ou pega o pedido pendente do usuário
        pedido, criado = Pedido.objects.get_or_create(
            cliente=usuario,
            status='Pendente'
        )

        # Adiciona a arte ao pedido
        pedido.artes.add(arte)

        # Atualiza o total agora que a ManyToMany existe
        pedido.total = pedido.calcular_total()
        pedido.save()

        return redirect('galeria')

    
# Lista pedidos do usuarios
class MeusPedidosView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'galeriaapp/meus_pedidos.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        # Só mostra os pedidos do usuário logado, do mais recente para o mais antigo
        return Pedido.objects.filter(cliente=self.request.user,status='Pendente').order_by('-data_criacao')
    
# Finaliza
class FinalizarPedidoView(LoginRequiredMixin, View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
        pedido.status = 'Entregue'
        pedido.save()
        return redirect('meus_pedidos')

class ArtesCompradasView(LoginRequiredMixin, ListView):
    model = Arte
    template_name = 'galeriaapp/artes_compradas.html'
    context_object_name = 'artes'

    def get_queryset(self):
        # Pega todas as artes dos pedidos concluídos do usuário
        return Arte.objects.filter(pedido__cliente=self.request.user, pedido__status='Entregue').distinct()

# Admin ----------------------------------------------------------------------------
class ArteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Arte
    template_name = 'galeriaapp/arte_list.html'  
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
    
    def test_func(self):
        # só admin ou staff podem acessar /lista/
        return self.request.user.is_staff

class ArteCreateView(CreateView):
    model = Arte
    fields = ['nome', 'categoria', 'preco', 'imagem', 'descricao']
    template_name = 'galeriaapp/arte_form.html'
    success_url = reverse_lazy('arte_list')

class ArteUpdateView(UpdateView):
    model = Arte
    fields = ['nome', 'categoria', 'preco', 'imagem', 'descricao']
    template_name = 'galeriaapp/arte_form.html'
    success_url = reverse_lazy('arte_list')

class ArteDeleteView(DeleteView):
    model = Arte
    template_name = 'galeriaapp/arte_confirm_delete.html'
    success_url = reverse_lazy('arte_list')