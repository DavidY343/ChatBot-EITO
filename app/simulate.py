from openai import OpenAI
import os
import django
import sys
import json
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from app.models import SimulatedUser

USE_MOCK = False  # Set to True to use mock data instead of OpenAI

def get_favorite_foods():
    """ChatGPT B: returns exactly 3 favorite foods in JSON format."""
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a person giving your top 3 favorite foods."},
            {"role": "user", "content": "Give exactly 3 favorite foods in JSON array format. "
                                    "30% of the time, they should be vegetarian or vegan (no meat, no fish). "
                                    "Example: [\"salad\",\"pasta\",\"tofu\"] or [\"pizza\",\"sushi\",\"chocolate\"]"}
        ],
        max_tokens=60,
        temperature=0.9
    )
    text = resp.choices[0].message.content.strip()
    try:
        foods = json.loads(text)
        if len(foods) != 3:
            foods = foods[:3] + ["unknown"]*(3-len(foods))
    except Exception as e:
        print("JSON parse error:", e)
        foods = ["unknown","unknown","unknown"]
    return foods

def verify_vegetarian(favorites):
    """ChatGPT C: Detects if the user is vegetarian or vegan."""
    prompt = f"""
    You are a food expert. Determine if a person is vegan, vegetarian, or non-vegetarian based on these 3 favorite foods: {favorites}
    Respond with only one word: 'vegan', 'vegetarian', or 'non-vegetarian'.
    """
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        temperature=0
    )
    result = resp.choices[0].message.content.strip().lower()
    return result in ["vegan", "vegetarian"]

def simulate(n=10):
    for i in range(n):
        if USE_MOCK:
            sample_foods = ["pizza", "pasta", "sushi", "salad", "falafel", "steak", "tofu", "ramen", "curry", "paella"]
            favorites = random.sample(sample_foods, 3)
            is_veg = any(f in ["salad", "falafel", "tofu"] for f in favorites)
        else:
            favorites = get_favorite_foods()
            is_veg = verify_vegetarian(favorites)

        name = f"sim_user_{i+1}"
        SimulatedUser.objects.create(
            name=name,
            is_vegan_or_vegetarian=is_veg,
            favorites=favorites
        )
        print(f"{i+1}/{n} -> {name}: {favorites} veg={is_veg}")

if __name__ == "__main__":
    simulate()
