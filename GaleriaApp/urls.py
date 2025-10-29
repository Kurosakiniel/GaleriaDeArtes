from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import ArteListView, ArteCreateView, ArteUpdateView, ArteDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('lista/', ArteListView.as_view(), name='arte_list'),
    path('nova/', ArteCreateView.as_view(), name='arte-create'),
    path('<int:pk>/editar/', ArteUpdateView.as_view(), name='arte-update'),
    path('<int:pk>/deletar/', ArteDeleteView.as_view(), name='arte-delete'), # até aqui é só admin que vê
    path('login/', LoginView.as_view(template_name='paginas/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='arte_list'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)