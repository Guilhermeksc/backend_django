from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from api.views import FrontendAppView

def home_view(request):
    return HttpResponse("Bem-vindo ao servidor Django!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Certifique-se de que o caminho do app está correto
    path('', home_view, name='home'),
    path('', FrontendAppView.as_view(), name='frontend'),  # Serve o frontend Angular
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
