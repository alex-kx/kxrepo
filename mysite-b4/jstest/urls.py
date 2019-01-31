from django.urls import path
from . import views



urlpatterns = [
    path('jstestindex/', views.detail),
    path('jstest1/', views.index),
    path('UploadExcel/', views.UploadExcel),
    path('echartstest/', views.echartstest),
    path('bootstrap/', views.bootstrap)
]