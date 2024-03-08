from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OnayUploadedModel(models.Model):
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
#----------------------------------------------------------------------------------- onay kayit defteri model  
class OnayRegisterModel(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    onay_no = models.CharField(max_length = 100)
    onay_aciklama = models.CharField(max_length = 100, default='my_default_value')
    #burda alani datefield sectik ve 'register_onay.html input olarak date yaptik. defter_onay_list.html icinde ise {{bilgi.onay_tarih|date:"d.m.Y"}} seklinde formatladik
    onay_tarih = models.DateField(default=datetime.now) 
    onay_odemetutar = models.CharField(max_length = 20)
    onay_parabirimi = models.CharField(max_length = 20)
    onay_odemeyolu = models.CharField(max_length = 20)
    def __str__(self):
        return f"kullanici+ {self.username} Belgeno+: {self.onay_no} Aciklama+: {self.onay_aciklama} Tarih+: {self.onay_tarih} Odeme Tutrari+: {self.onay_odemetutar} Para Birimi+: {self.onay_parabirimi} Odeme yolu+: {self.onay_odemeyolu}"


