from django.urls import path

from . import views

app_name = "movies_auth"
urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_out/', views.log_out, name='log_out'),
]
