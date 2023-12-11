from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from core.models import BaseModel


class Recipe(BaseModel):
    """Recipe object"""
    name = models.CharField(max_length=255, verbose_name='Name', help_text='Name of the recipe')
    description = models.TextField(
        verbose_name='Description', help_text='Description of the recipe', blank=True, null=True
    )
    ingredients = models.TextField(verbose_name='Ingredients', help_text='Ingredients of the recipe')
    instructions = models.TextField(verbose_name='Directions', help_text='Instructions of the recipe')
    prep_time = models.DurationField(
        verbose_name='Prep Time', help_text='Preparation time of the recipe',
        validators=[
            MinValueValidator(limit_value=timezone.timedelta(minutes=1),
                              message='Preparation time must be equal to or greater than 1 minute.')
        ]
    )
    cook_time = models.DurationField(
        verbose_name='Cook Time', help_text='Cooking time of the recipe',
        validators=[
            MinValueValidator(limit_value=timezone.timedelta(minutes=0),
                              message='Cooking time must be equal to or greater than 0 minutes.')
        ]
    )
    servings = models.IntegerField(
        verbose_name='Servings', help_text='Servings of the recipe', default=1,
        validators=[MinValueValidator(limit_value=1, message='Servings must be equal to or greater than 1.')]
    )
    chef = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Chef', help_text='Chef who created the recipe',
        related_name='recipes',
    )

    def __str__(self):
        return self.name

    def validate(self):
        if self.chef is None:
            raise ValueError('Recipe must be associated with a chef')
