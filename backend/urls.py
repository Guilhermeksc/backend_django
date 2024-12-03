from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from core.views import IndexView  # Certifique-se de que a app 'core' está criada e incluída no INSTALLED_APPS

urlpatterns = [
    path('admin/', admin.site.urls),
    # Adicione outras rotas de API aqui, se necessário
]

# Adicionar as rotas de arquivos estáticos
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Rota de captura geral para servir o Angular
urlpatterns += [
    re_path(r'^.*$', IndexView.as_view(), name='index'),
]
