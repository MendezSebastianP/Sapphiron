from django.urls import path
from . import views

#app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='chat_home'),  # Home page
    path('response/', views.chat_response, name='chat_response'),  # Chat response API
]