from django.views.generic import TemplateView
from django.http import Http404
import os
from django.conf import settings

class FrontendAppView(TemplateView):
    template_name = "index.html"  # Agora aponta diretamente para 'index.html' em 'static'

    def get(self, request, *args, **kwargs):
        # Verifica o caminho real do template
        template_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], self.template_name)
        if not os.path.exists(template_path):
            raise Http404(f"Template não encontrado: {template_path}")
        return super().get(request, *args, **kwargs)
