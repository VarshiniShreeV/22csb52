from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_shorturl, name='create_shorturl'), 
    path('<str:shortcode>/', views.get_shortinfo, name='get_shortinfo'),  
]
