from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('chat/', views.chat_response, name='chat-response'),  # Chat response API
]