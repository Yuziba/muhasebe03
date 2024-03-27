from django.contrib import admin

# Register your models here..
#--------------------admin panel ayarlari
from .models import OnayRegisterModel, ZiraatRegisterModel

admin.site.register(OnayRegisterModel)
admin.site.register(ZiraatRegisterModel)

#------------------------------------------------