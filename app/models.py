from django.db import models

class SimulatedUser(models.Model):
    name = models.CharField(max_length=200)
    is_vegan_or_vegetarian = models.BooleanField(default=False)
    favorites = models.JSONField(default=list)  # list of 3 foods
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    session_id = models.CharField(max_length=255)  # unique_ID
    role = models.CharField(max_length=20)  # "system", "user", "assistant"
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.session_id} - {self.role}: {self.content[:30]}"
