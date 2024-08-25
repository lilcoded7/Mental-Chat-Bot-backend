import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from bot.dataset import dataset
from difflib import SequenceMatcher
import random




def chatbot(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        response = get_response(user_message)
        return render(request, 'chatbot.html', {'response': response})
    return render(request, 'chatbot.html')

def get_response(user_message):
    user_message = user_message.lower()
    best_match = None
    best_ratio = 0

    for intent in dataset[0]["intents"]:
        for pattern in intent['patterns']:
            ratio = SequenceMatcher(None, user_message, pattern.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = intent

    if best_match and best_ratio > 0.6:
        return random.choice(best_match['responses'])
    else:
        return "I'm sorry, I don't understand. Could you please rephrase?"