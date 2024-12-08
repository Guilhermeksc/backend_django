from django.views.generic import TemplateView
from django.http import Http404
from django.conf import settings
from django.http import HttpResponse
import os
import subprocess
import shutil
from zipfile import ZipFile

class FrontendAppView(TemplateView):
    template_name = "index.html"  # Agora aponta diretamente para 'index.html' em 'static'

    def get(self, request, *args, **kwargs):
        # Verifica o caminho real do template
        template_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], self.template_name)
        if not os.path.exists(template_path):
            raise Http404(f"Template não encontrado: {template_path}")
        return super().get(request, *args, **kwargs)

def consultar_pdf(request):
    valor = request.GET.get('valor', '')

    if not valor:
        return HttpResponse("Valor não fornecido.", status=400)

    try:
        template_path = os.path.join(settings.BASE_DIR, 'api', 'templates', 'template.odt')
        if not os.path.exists(template_path):
            return HttpResponse("Template não encontrado.", status=404)

        temp_dir = os.path.join(settings.BASE_DIR, 'api', 'templates', 'temp_odt')
        temp_odt_path = os.path.join(settings.BASE_DIR, 'api', 'templates', 'temp.odt')
        temp_pdf_path = os.path.join(settings.BASE_DIR, 'api', 'templates', 'temp.pdf')

        # Limpar a pasta temporária e remover arquivos anteriores
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)

        if os.path.exists(temp_odt_path):
            os.remove(temp_odt_path)
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

        # Copiar template
        shutil.copy(template_path, temp_odt_path)

        # Extrair ODT
        with ZipFile(temp_odt_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        content_xml_path = os.path.join(temp_dir, 'content.xml')
        if not os.path.exists(content_xml_path):
            return HttpResponse("Arquivo content.xml não encontrado.", status=500)

        # Substituir placeholder
        with open(content_xml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('{{valor}}', valor)
        with open(content_xml_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Recriar ODT
        odt_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, temp_dir)
                odt_files.append((full_path, rel_path))

        with ZipFile(temp_odt_path, 'w') as zipf:
            for full_path, rel_path in odt_files:
                zipf.write(full_path, arcname=rel_path)

        # Caminho completo do LibreOffice no Windows
        libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
        if not os.path.exists(libreoffice_path):
            return HttpResponse("LibreOffice não encontrado no caminho especificado.", status=500)

        # Converter ODT em PDF
        subprocess.run([
            libreoffice_path, "--headless", "--convert-to", "pdf", temp_odt_path, "--outdir", os.path.dirname(temp_pdf_path)
        ], check=True)

        if not os.path.exists(temp_pdf_path):
            return HttpResponse("Falha na geração do PDF.", status=500)

        with open(temp_pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="resultado.pdf"'

        # Limpar arquivos temporários
        shutil.rmtree(temp_dir, ignore_errors=True)
        if os.path.exists(temp_odt_path):
            os.remove(temp_odt_path)
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

        return response

    except subprocess.CalledProcessError as e:
        return HttpResponse("Erro ao converter o arquivo ODT para PDF.", status=500)

    except Exception as e:
        return HttpResponse(f"Erro interno do servidor: {e}", status=500)