from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SimulatedUser
from .serializers import SimulatedUserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
import os


def home_page(request):
    return render(request, 'app/index.html')

def chat_page(request):
    return render(request, 'app/chat.html')

@login_required
def dashboard_page(request):
    return render(request, 'app/dashboard.html')

class VeganUsersView(APIView):
    def get(self, request):
        users = SimulatedUser.objects.filter(is_vegan_or_vegetarian=True)
        serializer = SimulatedUserSerializer(users, many=True)
        return Response(serializer.data)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a vegan chatbot assistant."},
                {"role": "user", "content": user_message},
            ],
            temperature=0.9,
            max_tokens=150
        )

        bot_message = resp.choices[0].message.content
        return JsonResponse({"message": bot_message})
    return JsonResponse({"error": "POST method required"}, status=400)

