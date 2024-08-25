from django.db import models
from django.contrib.auth.models import User

class MentalHealthResource(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class SelfCareTip(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:50]

class ProfessionalSupport(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.specialization}"

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    mood = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Chat with {self.user.username} at {self.timestamp}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_bot = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.content[:50]}"