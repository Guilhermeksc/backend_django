from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.http import Http404
from django.conf import settings
import os
import logging

class FrontendAppView(TemplateView):
    template_name = "index.html"  # Agora aponta diretamente para 'index.html' em 'static'

    def get(self, request, *args, **kwargs):
        # Verifica o caminho real do template
        template_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], self.template_name)
        if not os.path.exists(template_path):
            raise Http404(f"Template não encontrado: {template_path}")
        return super().get(request, *args, **kwargs)

logger = logging.getLogger(__name__)
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permite acesso sem autenticação

    def post(self, request):
        username = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        logger.info("Dados recebidos para registro: %s", {"username": username, "email": email})

        if User.objects.filter(username=username).exists():
            logger.warning("Usuário já existe: %s", username)
            return Response({'detail': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        logger.info("Usuário criado com sucesso: %s", {"username": username, "email": email})
        return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Permite acesso sem autenticação

    def post(self, request):
        logger.info("Dados recebidos: %s", request.data)

        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            logger.warning("Email ou senha ausente.")
            return Response({'detail': 'Email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user:
            logger.info("Usuário autenticado: %s", email)
            refresh = RefreshToken.for_user(user)
            return Response({
                'name': user.username,
                'token': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        logger.warning("Credenciais inválidas para: %s", email)
        return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)