from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator

#----------------------------------------------------------------------------------- onay belgesi yukleme model  
class OnayUploadedModel(models.Model):
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
#----------------------------------------------------------------------------------- onay kayit defteri model  
class OnayRegisterModel(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    onay_no = models.CharField(max_length = 4)
    onay_aciklama = models.CharField(max_length = 110, default='my_default_value')
    #burda alani datefield sectik ve 'register_onay.html input olarak date yaptik. defter_onay_list.html icinde ise {{bilgi.onay_tarih|date:"d.m.Y"}} seklinde formatladik
    onay_tarih = models.DateField() #auto_now_add ile kullanci deger girmese bile otomatik tarih atamasi yapar
    onay_odemetutar = models.CharField(max_length = 20)
    #onay_odemetutar = models.IntegerField(validators=[MaxValueValidator(10000000000)])
    onay_parabirimi = models.CharField(max_length = 20)
    onay_odemeyolu = models.CharField(max_length = 20)

    def clean(self):
        if not self.onay_tarih:
            raise ValidationError({'onay_tarih': 'Tarih alanı boş bırakılamaz.'})
        
    def __str__(self):
        return f"kullanici+ {self.username} Belgeno+: {self.onay_no} Aciklama+: {self.onay_aciklama} Tarih+: {self.onay_tarih} Odeme Tutrari+: {self.onay_odemetutar} Para Birimi+: {self.onay_parabirimi} Odeme yolu+: {self.onay_odemeyolu}"

#----------------------------------------------------------------------------------- onay belgesi yukleme model  
class ZiraatUploadModel(models.Model):
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file.name  

#----------------------------------------------------------------------------------- ziraat talimat kayit defteri model  
class ZiraatRegisterModel(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #sira no yazmadik cunku onu veri tabaninda islemeyecegim
    ziraat_tarih = models.DateField()
    ziraat_firma_adi = models.CharField(max_length = 100) #------------------html kisminda daha da kislatilabilir
    ziraat_muhasebe_belge_no = models.CharField(max_length = 10)
    ziraat_aciklama = models.CharField(max_length = 150) #------------------------------------html kisminda sinirlandirabiliriz
    ziraat_tutar = models.CharField(max_length = 20)
    ziraat_para_birimi = models.CharField(max_length = 20)

    def __str__(self):
        return f"Kullanıcı+ {self.username} Tarih+: {self.ziraat_tarih} Firma Adı+: {self.ziraat_firma_adi} Muhasebe Belge No+: {self.ziraat_muhasebe_belge_no} Açıklama+: {self.ziraat_aciklama} Ödeme Tutarı+: {self.ziraat_tutar} Para Birimi+: {self.ziraat_para_birimi} "    











