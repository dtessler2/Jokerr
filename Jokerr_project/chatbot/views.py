# chatbot/views.py
import openai
from openai import OpenAI
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

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
            print("Request body:", request.body)
            data = json.loads(request.body)
            category = data.get("message")
            if not is_valid_category(category):
                return JsonResponse({"reply": "Invalid joke category"})

            '''
            # Identity
            You are a helpful assistant the produces jokes
            
            # Instructions
            Only produce jokes that are family-friendly and don't have
            any adult content.
            Your response should be 1-3 sentences.
            '''
            response = client.responses.create(
                model="gpt-4.1",
                instructions="Talk in a family-friendly manner and filter out all adult content. Your response should be 1-3 sentences long.",
                input=f"Write a joke based on this category: {category}"
            )

            reply = response.output[0].content[0].text
            return JsonResponse({'reply': reply})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({'error': 'POST request required'}, status=400)

def is_valid_category(request):
    valid_categories = ["knock-knock", "knock knock", "riddle", "pun", "one-liner", "one liner", "political", "dad", "corny", "yeshivish"]
    if request.strip().lower() in valid_categories:
        return True
    return False

