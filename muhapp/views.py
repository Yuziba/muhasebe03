from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse,  Http404
from django.views.generic import TemplateView   
from . import models
import mimetypes

#-------------------------------------------------------------------------------------------------------------------------- Ana Sayfa 
class MainView(TemplateView):
    template_name = 'muhapp/main.html'

#---------------------------------------------------------------------------------------------------------------------------- SignUp
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

#----------------------------------------------------------------------------------------------------------------- Onay Yukleme View 
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

#----------------------------------------------------------------------------------------------------- Onay belgelerini sayfadan silme 
def onay_delete_view(request, file_id):
    file_to_delete = get_object_or_404(models.OnayUploadedModel, id=file_id)
    file_to_delete.delete()
    return redirect('muhapp:onay_list')

#--------------------------------------------------------------------------------------------------------------- Onay belgele indirme
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


#---------------------------------------------------------------------------------------------------------- Kayit Defterleri 1. sayfasi
class Belge_Kayit_View(TemplateView):
    template_name = 'muhapp/defterler.html'

#----------------------------------------------------------------------------------------------------------- Onay Kayit Defteri sayfasi
class Onay_Kayit_View(TemplateView):
    template_name = 'muhapp/defter_onay_list.html'

#----------------------------------------------------------------------------------------- Ziraat Bankasi Talimat Kayit Defteri sayfasi
class Ziraat_Kayit_View(TemplateView):
    template_name = 'muhapp/defter_ziraat.html'

#------------------------------------------------------------------------------------------ Demirbank Talimat Duz Kayit Defteri sayfasi
class Demir_Duz_Kayit_View(TemplateView):
    template_name = 'muhapp/defter_dbank_duz.html'

#------------------------------------------------------------------------------------------- Demirbank Talimat YF Kayit Defteri sayfasi
class Demir_YF_Kayit_View(TemplateView):
    template_name = 'muhapp/defter_dbank_yf.html'

#--------------------------------------------------------------------------------------- Onay Defter Kayit Defteri (New Window) sayfasi
class Register_Onay_View(TemplateView):
    template_name = 'muhapp/register_onay.html'


#--------------------------------------------------------------------------------- Onay Defteri sayfasinda bilgileri gostermek icin
def defter_onay_list_view(request):
    list_onay_bilgiler = models.OnayRegisterModel.objects.all()
    list_onay_bilgiler = {"list_onay_bilgiler":list_onay_bilgiler}
    return render(request, 'muhapp/defter_onay_list.html', context=list_onay_bilgiler)
    #return render(request, 'muhapp/defter_onay_list.html', {'onay_bilgiler': onay_bilgiler})

#----------------------------------------------------------------------------------------------- Onay Defter Kayit Defteri (New Window)
def register_onay_dataBase_kayit(request):
    if request.method == 'POST':
        onay_no         = request.POST.get("onay_no", "")
        onay_aciklama   = request.POST.get("onay_aciklama", "")
        onay_tarih      = request.POST.get("onay_tarih", "")
        onay_odemetutar = request.POST.get("onay_odemetutar", "")
        onay_parabirimi = request.POST.get("onay_parabirimi", "")
        onay_odemeyolu  = request.POST.get("onay_odemeyolu", "")
        #print("--------------" ,onay_no, onay_aciklama, onay_tarih, onay_odemetutar, onay_parabirimi, onay_odemeyolu )
        # Bu bilgileri veritabanına kaydet
        models.OnayRegisterModel.objects.create(username        =request.user, 
                                                onay_no         =onay_no, 
                                                onay_aciklama   =onay_aciklama, 
                                                onay_tarih      =onay_tarih, 
                                                onay_odemetutar =onay_odemetutar, 
                                                onay_parabirimi = onay_parabirimi,
                                                onay_odemeyolu  =onay_odemeyolu,)
        return redirect(reverse('muhapp:list_onay_bilgiler'))
    else:
        return render(request, 'muhapp/main.html')







