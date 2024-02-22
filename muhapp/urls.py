from django.urls import path
from . import views

app_name = 'muhapp'

urlpatterns = [
    path('', views.MainView.as_view(), name="main"),
    path('onaylar/', views.onay_upload_view, name="onay_upload")
]

