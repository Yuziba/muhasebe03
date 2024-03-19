

#--------------------------------------------------------------------OnayRegisterModel modeline dayalı bir ModelForm olusturduk.
from django import forms
from .models import OnayRegisterModel

class OnayRegisterModelForm(forms.ModelForm):
    class Meta:
        model = OnayRegisterModel
        fields = ['onay_no', 'onay_aciklama', 'onay_tarih', 'onay_odemetutar', 'onay_parabirimi', 'onay_odemeyolu']
#------------------------------------------------------------------------------------------------------------------------------
        
#----------------------------------------------------------------------------defter onay list ekraninda radio buton yapmak icin.      



    