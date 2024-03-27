

#--------------------------------------------------------------------OnayRegisterModel modeline dayalı bir ModelForm olusturduk.
from django import forms
from .models import OnayRegisterModel


class OnayRegisterModelForm(forms.ModelForm):
    class Meta:
        model = OnayRegisterModel
        fields = ['onay_no', 'onay_aciklama', 'onay_tarih', 'onay_odemetutar', 'onay_parabirimi', 'onay_odemeyolu']

from .models import ZiraatRegisterModel

class ZiraatRegisterModelForm(forms.ModelForm):
    class Meta:
        model = ZiraatRegisterModel
        fields = ['ziraat_tarih', 'ziraat_firma_adi', 'ziraat_muhasebe_belge_no', 'ziraat_aciklama', 'ziraat_tutar', 'ziraat_para_birimi']


#------------------------------------------------------------------------------------------------------------------------------
        
#----------------------------------------------------------------------------defter onay list ekraninda radio buton yapmak icin.      



    