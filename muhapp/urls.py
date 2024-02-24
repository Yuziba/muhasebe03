from django.urls import path
from . import views

app_name = 'muhapp'

urlpatterns = [
    path('', views.MainView.as_view(), name="main"),
    path('defterler/', views.Belge_Kayit_View.as_view(), name="defterler"),
    path('defter_onay', views.Onay_Kayit_View.as_view(), name="defter_onay"),
    path('onay_upload/', views.onay_upload_view, name="onay_upload"),
    path('onay_list/', views.onay_list_view, name='onay_list'),
    path('onay_delete/<int:file_id>/', views.onay_delete_view, name='onay_delete'),
    path('onay_download/<int:file_id>/', views.onay_download_view, name='onay_download'),

]

