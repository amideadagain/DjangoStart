from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "movies_auth"
urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_out/', views.log_out, name='log_out'),
    path('api/sign_up', views.ApiSignUp.as_view(), name='api_sign_up'),
    path('api/sign_in', views.ApiSignIn.as_view(), name='api_sign_in'),
    path('api/log_out', views.ApiLogout.as_view(), name='api_log_out'),
    # path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
