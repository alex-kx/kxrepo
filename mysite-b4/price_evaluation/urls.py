from django.urls import path
from . import views

urlpatterns = [

    path('insert_price_data/', views.insert_price_data, name='insert_price_data'),

    path('price_evaluation/', views.price_evaluation, name='price_evaluation'),

    path('retrieve_ref_price/', views.retrieve_ref_price, name='retrieve_ref_price'),

]