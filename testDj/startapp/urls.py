from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='startapp-home'),
    path('about/', views.about, name='startapp-about'),
]