from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Ingredient, Recipe


class ModelTests(TestCase):
    """Models tests"""

    def test_model_recipe_str(self):
        """Test correct string cast"""
        recipe = Recipe.objects.create(
            name='Pizza napolitana',
            description='Classic napolitana pizza, delicious'
        )
        self.assertEqual(str(recipe), recipe.name)

    def test_model_ingredient_str(self):
        """Test correct string cast"""
        recipe = Recipe.objects.create(
            name='Pizza napolitana',
            description='Classic napolitana pizza, delicious'
        )
        ingredient = Ingredient.objects.create(
            name='Tomato',
            recipe=recipe
        )
        self.assertEqual(str(ingredient), ingredient.name)


