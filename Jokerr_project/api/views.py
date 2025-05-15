from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import json
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot_response(request):
    if request.method == 'POST':
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

    return JsonResponse({'error': 'POST request required'}, status=400)