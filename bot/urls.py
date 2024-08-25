from django.urls import path
from bot.views import *

urlpatterns = [
    path('chatbot/', chatbot, name='chatbot'),
]