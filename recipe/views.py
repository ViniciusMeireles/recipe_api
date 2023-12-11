from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .filters import RecipeFilter
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for recipes.
    """
    model = Recipe
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer(self, *args, **kwargs):
        kwargs['chef'] = self.request.user
        return super(RecipeViewSet, self).get_serializer(*args, **kwargs)
