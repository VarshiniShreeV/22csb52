
from django.contrib import admin
from django.urls import path, include
from core import views as short_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shorturls/', include('core.urls')),     
    path('<str:shortcode>/', short_views.redirect_short, name='redirect_short'), 
]

