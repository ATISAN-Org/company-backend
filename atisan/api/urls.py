from django.urls import path
from .views import register_api, login_api


urlpatterns = [
    path('register/', register_api, name='api_register'),
    path('login/', login_api, name='api_login'),
]
