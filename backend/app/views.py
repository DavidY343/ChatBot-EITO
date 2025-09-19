from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SimulatedUser
from .serializers import SimulatedUserSerializer
from .simulate import simulate
from collections import Counter
from openai import OpenAI
import os
import json


def home_page(request):
    return render(request, 'app/index.html')


def chat_page(request):
    return render(request, 'app/chat.html')


@login_required
def dashboard_page(request):
    return render(request, 'app/dashboard.html')


# Endpoint: Protected
class VeganUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = SimulatedUser.objects.filter(is_vegan_or_vegetarian=True)
        serializer = SimulatedUserSerializer(users, many=True)
        return Response(serializer.data)


# Endpoint: Run simulation
@api_view(["POST"])
@permission_classes([IsAdminUser])
def run_simulation(request):
    count = int(request.data.get("count", 100))
    simulate(count)
    return Response({"status": f"Simulated {count} users"})


# Endpoint: Stats (additional)
class StatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total = SimulatedUser.objects.count()
        veg = SimulatedUser.objects.filter(is_vegan_or_vegetarian=True).count()
        non_veg = total - veg

        # TOP favorite foods
        foods = []
        for u in SimulatedUser.objects.all():
            if u.favorite_foods:
                try:
                    foods.extend(u.favorite_foods.split(","))
                except AttributeError:
                    pass
        top_foods = Counter([f.strip() for f in foods if f.strip()]).most_common(5)

        return Response({
            "total_users": total,
            "vegans_or_vegetarians": veg,
            "non_veg": non_veg,
            "top_foods": top_foods
        })


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
