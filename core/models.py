from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """Base model for all models in the project."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for BaseModel."""
        abstract = True
        ordering = ['-created_at', '-updated_at']
