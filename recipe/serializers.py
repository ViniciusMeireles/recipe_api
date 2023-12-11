from rest_framework import serializers
from rest_framework.fields import empty

from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipe objects
    """
    chef = serializers.ReadOnlyField(source='chef.username')

    class Meta:
        model = Recipe
        fields = '__all__'
        extra_kwargs = {
            'prep_time': {'help_text': 'Preparation time of the recipe, format: HH:MM:SS'},
            'cook_time': {'help_text': 'Cooking time of the recipe, format: HH:MM:SS'},
            'servings': {'min_value': 1},
        }

    def __init__(self, instance=None, data=empty, chef=None, **kwargs):
        super(RecipeSerializer, self).__init__(instance=instance, data=data, **kwargs)
        # If chef is not passed as an argument, try to get it from the request

        if not chef:
            request = self.context.get('request')
            try:
                chef = request.user if request else None
            except:
                chef = None
        elif not chef and instance:
            chef = instance.chef
        self.chef = chef

    def validate(self, attrs):
        # Check if chef is set
        if not self.chef and not attrs.get('chef'):
            raise serializers.ValidationError('Only chefs can register recipes')
        elif self.chef and not attrs.get('chef'):
            attrs['chef'] = self.chef
        return attrs

    @property
    def validated_data(self):
        data = super(RecipeSerializer, self).validated_data
        if self.chef:
            data['chef'] = self.chef
        return data
