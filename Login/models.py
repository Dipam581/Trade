from django.contrib.auth.models import User
from django.db import models
import uuid

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return self.user.username
