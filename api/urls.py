from django.urls import path
from .views import FrontendAppView, RegisterView, LoginView

urlpatterns = [
    path('', FrontendAppView.as_view(), name='frontend'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'), 
]