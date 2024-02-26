from django.urls import path
from . import views

app_name = 'muhapp'

urlpatterns = [
    path('', views.MainView.as_view(), name="main"),                                        #Ana Sayfa
    path('defterler/', views.Belge_Kayit_View.as_view(), name="defterler"),                 #Defterlerin Ana Sayfasi
    path('defter_onay_list', views.Onay_Kayit_View.as_view(), name="defter_onay_list"),     #Onay Belgesi Defteri sayfasi
    path('defter_ziraat', views.Ziraat_Kayit_View.as_view(), name="defter_ziraat"),         #Ziraat Belgesi Defteri sayfasi
    path('defter_dbank_duz', views.Demir_Duz_Kayit_View.as_view(), name="defter_dbank_duz"),#Demir Belgesi Defteri sayfasi
    path('defter_dbank_yf', views.Demir_YF_Kayit_View.as_view(), name="defter_dbank_yf"),   #Demir Belgesi Defteri sayfasi
    path('register_onay', views.Register_Onay_View.as_view(), name="register_onay"),        #register_onay sayfasi
    path('signup/', views.SignUpView.as_view(), name='signup'), 

    path('list_onay_bilgiler', views.defter_onay_list_view, name="list_onay_bilgiler"),  
    
    path('onay_upload/', views.onay_upload_view, name="onay_upload"),
    path('onay_list/', views.onay_list_view, name='onay_list'),
    path('onay_delete/<int:file_id>/', views.onay_delete_view, name='onay_delete'),
    path('onay_download/<int:file_id>/', views.onay_download_view, name='onay_download'),
    path('register_onay_dataBase_kayit', views.register_onay_dataBase_kayit, name="register_onay_dataBase_kayit"),

    

]

