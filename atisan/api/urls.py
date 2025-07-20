from django.urls import path
from .views import register_api, login_api,project_list


urlpatterns = [
    path('register/', register_api, name='api_register'),
    path('login/', login_api, name='api_login'),
    path('projects/', project_list, name='project-list')
]
