from django.shortcuts import render

# Create your views here.

# chatbot/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        # Simple echo response (you can implement actual chatbot logic here)
        response_message = f"You said: {user_message}"
        return JsonResponse({"response": response_message})
    return JsonResponse({"error": "Only POST requests are allowed"}, status=400)