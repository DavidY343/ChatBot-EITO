from rest_framework import serializers
from .models import SimulatedUser

class SimulatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatedUser
        fields = ['id','name','is_vegan_or_vegetarian','favorites','created_at']
