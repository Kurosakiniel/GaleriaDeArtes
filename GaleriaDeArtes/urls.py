"""
URL configuration for GaleriaDeArtes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from GaleriaApp.views import ArteListView, ArteCreateView, ArteUpdateView, ArteDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('arte_list/', ArteListView.as_view(), name='arte_list'),
    path('nova/', ArteCreateView.as_view(), name='arte-create'),
    path('<int:pk>/editar/', ArteUpdateView.as_view(), name='arte-update'),
    path('<int:pk>/deletar/', ArteDeleteView.as_view(), name='arte-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)