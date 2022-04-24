from django.db import models
from authApp.models import CustomUser

class Event(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(CustomUser, related_name='participants', blank=True)

    def __str__(self):
        return self.title
