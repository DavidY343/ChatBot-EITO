from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SimulatedUser, ChatMessage
from .serializers import SimulatedUserSerializer
from .simulate import simulate
from collections import Counter
from openai import OpenAI
import os
import json, uuid


def home_page(request):
    return render(request, 'app/index.html')


def chat_page(request):
    return render(request, 'app/chat.html')


def api_interface_page(request):
    return render(request, 'app/api.html')

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
    def get(self, request):
        try:
            veg_count = SimulatedUser.objects.filter(is_vegan_or_vegetarian=True).count()
            non_veg_count = SimulatedUser.objects.filter(is_vegan_or_vegetarian=False).count()

            # Top 5 foods
            all_foods = []
            for user in SimulatedUser.objects.all():
                all_foods.extend(user.favorites or [])

            top_foods = Counter(all_foods).most_common(5)

            return Response({
                'veg_count': veg_count,
                'non_veg_count': non_veg_count,
                'top_foods': top_foods
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# @csrf_exempt
# def chat_api(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         user_message = data.get("message", "")

#         resp = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a vegan chatbot assistant."},
#                 {"role": "user", "content": user_message},
#             ],
#             temperature=0.9,
#             max_tokens=150
#         )

#         bot_message = resp.choices[0].message.content
#         return JsonResponse({"message": bot_message})
#     return JsonResponse({"error": "POST method required"}, status=400)

# @csrf_exempt
# def chat_api(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST method required"}, status=400)

#     data = json.loads(request.body)
#     user_message = data.get("message", "")

#     # FIRST MESSAGE
#     if user_message == "__start__":
#         return JsonResponse({
#             "message": "Hi! 🍴 I'm your foodie assistant. Tell me your 3 favourite foods!"
#         })

#     # Noraml conversation
#     resp = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a foodie assistant. Be conversational and friendly."},
#             {"role": "user", "content": user_message},
#         ],
#         temperature=0.9,
#         max_tokens=150
#     )

#     bot_message = resp.choices[0].message.content
#     return JsonResponse({"message": bot_message})


# @csrf_exempt
# def chat_api(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST method required"}, status=400)

#     data = json.loads(request.body)
#     user_message = data.get("message", "")

#     # Retrieve history
#     history = request.session.get("chat_history", [])

#     # FIRST MESSAGE
#     if user_message == "__start__":
#         bot_message = "Hi! 🍴 I'm your foodie assistant. Tell me your 3 favourite foods!"
#         # Reset history
#         history = [
#             {"role": "system", "content": "You are a foodie assistant. Be conversational and friendly."},
#             {"role": "assistant", "content": bot_message},
#         ]
#         request.session["chat_history"] = history
#         return JsonResponse({"message": bot_message})

#     # Build the full prompt
#     history.append({"role": "user", "content": user_message})

#     resp = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=history,
#         temperature=0.9,
#         max_tokens=150
#     )

#     bot_message = resp.choices[0].message.content

#     # Guardar respuesta en historial
#     history.append({"role": "assistant", "content": bot_message})
#     request.session["chat_history"] = history

#     return JsonResponse({"message": bot_message})

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    data = json.loads(request.body)
    user_message = data.get("message", "")
    session_id = request.session.get("chat_session_id")

    if not session_id:
        session_id = str(uuid.uuid4())
        request.session["chat_session_id"] = session_id

    # First message
    if user_message == "__start__":
        bot_message = "Hi! 🍴 I'm your foodie assistant. Tell me your 3 favourite foods!"

        # Reset history in DB
        ChatMessage.objects.filter(session_id=session_id).delete()

        ChatMessage.objects.create(session_id=session_id, role="system", content="You are a foodie assistant. Be conversational and friendly.")
        ChatMessage.objects.create(session_id=session_id, role="assistant", content=bot_message)

        return JsonResponse({"message": bot_message})

    # Sabe message
    ChatMessage.objects.create(session_id=session_id, role="user", content=user_message)

    # Retrieve conversation
    history = ChatMessage.objects.filter(session_id=session_id).values("role", "content")

    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=list(history),
        temperature=0.9,
        max_tokens=150
    )

    bot_message = resp.choices[0].message.content

    ChatMessage.objects.create(session_id=session_id, role="assistant", content=bot_message)

    return JsonResponse({"message": bot_message})