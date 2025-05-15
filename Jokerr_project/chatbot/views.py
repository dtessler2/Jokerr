# chatbot/views.py

import openai
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot_interface(request):
    return render(request, "chatbot/chatbot.html")

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        # Simple echo response (you can implement actual chatbot logic here)
        response_message = f"You said: {user_message}"
        return JsonResponse({"response": response_message})
    return JsonResponse({"error": "Only POST requests are allowed"}, status=400)

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get("message")

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            reply = response.choices[0].message["content"]
            return JsonResponse({'reply': reply})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({'error': 'POST request required'}, status=400)