from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from recipe.serializers import RecipeSerializer
from core.models import Ingredient, Recipe

from recipe import serializers


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-name')  # order by default

    def perform_create(self, serializer):
        recipe = Recipe.objects.get(id=self.request.data['recipe'])
        serializer.save(recipe=recipe)


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return self.queryset.all().order_by('-name')  # order by default
