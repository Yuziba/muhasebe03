from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse,  Http404
from django.views.generic import TemplateView   
from . import models
import mimetypes

#--------------------------------------------------------------------------------------------------------------------------- Ana Sayfa 
class MainView(TemplateView):
    template_name = 'muhapp/main.html'

#------------------------------------------------------------------------------------------------------------------- Onay Yukleme View 
def onay_upload_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Dosyayı işle ve veritabanına kaydet
            new_file = models.OnayUploadedModel(file=uploaded_file)
            new_file.save()

            
            return JsonResponse({'message': 'Dosya başarıyla yüklendi.'}, status=200)
        else:
            # Dosya yüklenmediğinde hata yanıtı
            return JsonResponse({'error': 'Dosya yüklenirken bir hata oluştu.'}, status=400)
    else:
        # POST isteği dışında gelen isteklere hata yanıtı
        return JsonResponse({'error': 'Geçersiz istek yöntemi.'}, status=405)
    
#--------------------------------------------------------------------------------------------------------------- Onay sayfada gosterme 
def onay_list_view(request):
    files = models.OnayUploadedModel.objects.all()  # models.py'deki modele göre
    return render(request, 'muhapp/onaylar.html', {'files': files})   

#------------------------------------------------------------------------------------------------------- Onay belgelerini sayfadan silme 
def onay_delete_view(request, file_id):
    file_to_delete = get_object_or_404(models.OnayUploadedModel, id=file_id)
    file_to_delete.delete()
    return redirect('muhapp:onay_list')

#----------------------------------------------------------------------------------------------------------------- Onay belgele indirme
def onay_download_view(request, file_id):
    file_instance = get_object_or_404(models.OnayUploadedModel, id=file_id)
    file_path = file_instance.file.path

    # MIME türünü belirle
    mime_type, encoding = mimetypes.guess_type(file_path)

    # Dosyayı aç ve kullanıcıya gönder
    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
            return response
    except FileNotFoundError:
        raise Http404("Belirtilen dosya bulunamadı.")


#------------------------------------------------------------------------------------------------------------- Kayit Defterleri sayfasi
class Belge_Kayit_View(TemplateView):
    template_name = 'muhapp/defterler.html'

