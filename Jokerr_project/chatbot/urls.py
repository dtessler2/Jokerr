# chatbot/urls.py

from django.urls import path
from . import views
from django.shortcuts import render


def home(request):
    return render(request, 'chatbot/chatbot.html')

urlpatterns = [
    path('', home, name='home'),  # This will serve as the main homepage
    path('get-joke/', home, name='get_joke'), # this page does the same thing as standard home page
    path('chat/', views.chatbot_response, name='chatbot_response'),
]