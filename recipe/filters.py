import django_filters

from recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    """
    Filter for Recipe objects
    """
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='Recipe name',
        help_text='Name of the recipe',
    )
    chef_username = django_filters.CharFilter(
        field_name='chef__username', lookup_expr='iexact', label='Chef Username',
        help_text='Chef username of the recipe',
    )

    class Meta:
        model = Recipe
        fields = ['name', 'chef_username']
