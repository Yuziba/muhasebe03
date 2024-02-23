from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,  Http404
from django.views.generic import TemplateView   
from . import models

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

            # Başarılı yanıt
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



