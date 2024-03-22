from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse,  Http404
from django.views.generic import TemplateView   
from . import models
import mimetypes
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, FloatField  # Burada Sum fonksiyonunu ekleyin
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
import datetime

#-------------------------------------------------------------------------------------------------------------------------- Ana Sayfa 
class MainView(TemplateView):
    template_name = 'muhapp/main.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bugunun_tarihi = timezone.now().date()
        tl_toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi, onay_parabirimi="Lira").aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
        
        # SOM için toplam tutar
        som_toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi, onay_parabirimi="Som").aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
        
        # Dolar için toplam tutar
        dolar_toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi, onay_parabirimi="Dolar").aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
        
        # Euro için toplam tutar
        euro_toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi, onay_parabirimi="Euro").aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
        
        toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi).aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
        
        context = {
        'bugunun_tarihi': bugunun_tarihi,
        'tl_toplam_tutar': tl_toplam_tutar,
        'som_toplam_tutar': som_toplam_tutar,
        'dolar_toplam_tutar': dolar_toplam_tutar,
        'euro_toplam_tutar': euro_toplam_tutar,
        'toplam_tutar': toplam_tutar,
    }
        
        return context
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


#----------------------------------------------------------------------------------- Onay Defteri sayfasinda bilgileri gostermek icin
def defter_onay_list_view(request):
    defter_onay_list = models.OnayRegisterModel.objects.all()
    defter_onay_list = {"defter_onay_list":defter_onay_list}
    return render(request, 'muhapp/defter_onay_list.html', context=defter_onay_list)
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
        # Bu bilgileri veritabanına kaydet
        models.OnayRegisterModel.objects.create(username        =request.user, 
                                                onay_no         =onay_no, 
                                                onay_aciklama   =onay_aciklama, 
                                                onay_tarih      =onay_tarih, 
                                                onay_odemetutar =onay_odemetutar, 
                                                onay_parabirimi = onay_parabirimi,
                                                onay_odemeyolu  =onay_odemeyolu,)
        #return redirect(reverse('muhapp:defter_onay_list'))
        #kayit butinuna tiklandiktan sonra pencere kapatma islemi ve yenileme2
        response = HttpResponse('<script>window.close(); window.opener.location.reload();</script>')
        return response
    else:
        return render(request, 'muhapp/main.html')
        

#--------------------------------------------------------------------------------------------------- Onay Defter Kayit silme
@login_required
def onay_list_delete_view(request, id):
    onay_bilgi = models.OnayRegisterModel.objects.get(pk=id)
    if request.user == onay_bilgi.username:                      #kontrol
        models.OnayRegisterModel.objects.filter(id=id).delete() #silme kodu
        return redirect('muhapp:defter_onay_list')                 #yonlendirme *ayni sayfa


#--------------------------------------------------------------------------------------------------- Onay Defter Kayit Editleme
def edit_onay_bilgi(request, id):
    onay_bilgi = get_object_or_404(models.OnayRegisterModel, pk=id)

    if request.method == 'POST':
        # POST verilerini al
        #onay_no = request.POST.get('onay_no')
        onay_aciklama = request.POST.get('onay_aciklama')
        onay_tarih = request.POST.get('onay_tarih')
        onay_odemetutar = request.POST.get('onay_odemetutar')
        onay_parabirimi = request.POST.get('onay_parabirimi')
        onay_odemeyolu = request.POST.get('onay_odemeyolu')

        # Modeli güncelle
        #onay_bilgi.onay_no = onay_no
        onay_bilgi.onay_aciklama = onay_aciklama
        onay_bilgi.onay_tarih = onay_tarih
        onay_bilgi.onay_odemetutar = onay_odemetutar
        onay_bilgi.onay_parabirimi = onay_parabirimi
        onay_bilgi.onay_odemeyolu = onay_odemeyolu
        onay_bilgi.save()

        return redirect('muhapp:defter_onay_list')

    return render(request, 'muhapp/edit_register_onay.html', {'onay_bilgi': onay_bilgi})
    


#--------------------------------------------------------------------------------------------------- belirli bi tarhteki toplam odeme tutarini gosterme
def filter_onay_list(request):
    onay_tarih = request.GET.get('onay_tarih_filter')
    onay_parabirimi = request.GET.get('onay_parabirimi_filter')
    
    my_filtered_data = models.OnayRegisterModel.objects.filter(onay_tarih=onay_tarih, onay_parabirimi=onay_parabirimi)
    toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=onay_tarih).aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']

    context = {
        'filtered_data': my_filtered_data,
        'toplam_tutar': toplam_tutar,
        # Diğer değişkenleri ekleyebilirsiniz
    }
    
    return render(request, 'muhapp/defter_onay_list.html', context)

#--------------------------------------------------------------------------------------------------- o gunku  toplam odeme tutarini anasayfada gosterme

def deneme(request):
    bugunun_tarihi = timezone.now().date()
    
    # TL için toplam tutar
    tl_toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi, onay_parabirimi="Lira").aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
    
    # SOM için toplam tutar
    som_toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi, onay_parabirimi="Som").aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
    
    # Dolar için toplam tutar
    dolar_toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi, onay_parabirimi="Dolar").aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
    
    # Euro için toplam tutar
    euro_toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi, onay_parabirimi="Euro").aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
    toplam_tutar = models.OnayRegisterModel.objects.filter(onay_tarih=bugunun_tarihi).aggregate(toplam_tutar=Sum('onay_odemetutar'))['toplam_tutar']
    context = {
        'bugunun_tarihi': bugunun_tarihi,
        'tl_toplam_tutar': tl_toplam_tutar,
        'som_toplam_tutar': som_toplam_tutar,
        'dolar_toplam_tutar': dolar_toplam_tutar,
        'euro_toplam_tutar': euro_toplam_tutar,
        'toplam_tutar': toplam_tutar,
    }
    
    return render(request, 'muhapp/deneme.html', context)

#------------------------------------------------------------------------------------------------------------ 
#                                                    Ziraatler
#------------------------------------------------------------------------------------------------------------ 
#----------------------------------------------------------------------------------------------------------------- Ziraat Yukleme View 
def ziraat_upload_view(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            new_file = models.ZiraatUploadModel(file=uploaded_file)
            new_file.save()
            return JsonResponse({'message': 'Dosya başarıyla yüklendi.' }, status=200)
        else:
            return JsonResponse({'error': 'Dosya yüklenirken bir hata oluştu.'}, status=400)
    else:
        return JsonResponse({'error' : 'Geçersiz istek yöntemi.'}, status=405)

#----------------------------------------------------------------------------------------------------------------- Ziraat Yuklenen begeleri listeleme    
def ziraat_list_view(request):
    ziraatBankaTalimatlari = models.ZiraatUploadModel.objects.all()
    return render(request, 'muhapp/ziraat.html', {'files':ziraatBankaTalimatlari})

#----------------------------------------------------------------------------------------------------------------- Ziraat Yuklenen begeleri silme
#----------------------------------------------------------------------------------------------------------------- Ziraat Yuklenen begeleri indirme   
#----------------------------------------------------------------------------------- ziraat Talimat kait Defteri sayfasinda bilgileri gostermek icin

def ziraat_defter_list_view(request):
    ziraat_defter_list_view = models.ZiraatUploadModel.objects.all()
    ziraat_defter_list_view = {"ziraat_defter_list_view":ziraat_defter_list_view}
    return render(request, 'muhapp/defter_ziraat.html', context=ziraat_defter_list_view)

