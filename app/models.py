from django.db import models

class SimulatedUser(models.Model):
    name = models.CharField(max_length=200)
    is_vegan_or_vegetarian = models.BooleanField(default=False)
    favorites = models.JSONField(default=list)  # list of 3 foods
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
