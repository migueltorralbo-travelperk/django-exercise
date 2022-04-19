from rest_framework import serializers
from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Override create for creating ingredients into the new recipe"""
        ingredients = validated_data.pop('ingredients', None)
        recipe = Recipe.objects.create(**validated_data)
        if ingredients:
            for ingredient in ingredients:
                Ingredient.objects.create(recipe=recipe, **ingredient)
        return recipe

    def update(self, instance, validated_data):
        """Override update for updating ingredients into the new recipe"""
        ingredients = validated_data.pop('ingredients', None)
        instance.ingredients.all().delete()

        if ingredients:
            for ingredient in ingredients:
                instance.ingredients.create(
                    name=ingredient['name'],
                    recipe=instance
                )

        super().update(instance, validated_data)
        return instance
