from django.urls import path
from . import views

app_name = 'muhapp'

urlpatterns = [
    path('', views.MainView.as_view(), name="main"),
    path('onay_upload/', views.onay_upload_view, name="onay_upload"),
    path('onay_list/', views.onay_list_view, name='onay_list'),
]

