# chatbot/views.py

from openai import OpenAI
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

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
            tools = [{
                "type": "function",
                "name": "is_valid_category",
                "description": "Returns a boolean value indicating whether or not the user-entered category is valid",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Joke category e.g knock-knock, riddle"
                        }
                    },
                "required": [
                    "category"
                ],
                "additionalProperties": False
                }
            }]
            data = json.loads(request.body)
            user_input = data.get("message")

            response = client.responses.create(
                model="gpt-4",
                input=[
                    {"role": "user", "content": user_input}
                ], tools=tools
            )

            reply = response.output
            return JsonResponse({'reply': reply})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({'error': 'POST request required'}, status=400)

def is_valid_category(request):
    valid_categories = ["knock-knock", "knock knock", "riddle", "pun", "one-liner", "one liner", "political", "dad", "corny"]
    data = json.loads(request.body)
    user_input = data.get("message")
    if user_input.trim().toLowerCase() in valid_categories:
        return True
    return False

