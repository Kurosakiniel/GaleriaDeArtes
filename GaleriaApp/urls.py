from django.urls import path
from .views import ArteListView, ArteCreateView, ArteUpdateView, ArteDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('lista/', ArteListView.as_view(), name='arte_list'),
    path('nova/', ArteCreateView.as_view(), name='arte-create'),
    path('<int:pk>/editar/', ArteUpdateView.as_view(), name='arte-update'),
    path('<int:pk>/deletar/', ArteDeleteView.as_view(), name='arte-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)