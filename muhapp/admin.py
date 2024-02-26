from django.contrib import admin

# Register your models here..
#--------------------admin panel ayarlari
from .models import OnayRegisterModel

admin.site.register(OnayRegisterModel)

#------------------------------------------------