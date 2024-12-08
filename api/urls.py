from django.urls import path
from .views import FrontendAppView, consultar_pdf

urlpatterns = [
    path('', FrontendAppView.as_view(), name='frontend'),
    path('consultar-pdf/', consultar_pdf, name='consultar_pdf'),
]
