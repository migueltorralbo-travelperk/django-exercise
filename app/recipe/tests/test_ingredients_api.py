from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient

from recipe.serializers import IngredientSerializer, RecipeSerializer
from core.models import Ingredient, Recipe

INGREDIENTS_URL = reverse('recipe:ingredient-list')
RECIPES_URL = reverse('recipe:recipe-list')


class RecipeApiTests(TestCase):

    def test_retrieve_recipes_list(self):
        recipe1 = Recipe.objects.create(name="Pizza napolitana", description="Traditional italian pizza")
        recipe2 = Recipe.objects.create(name="Paella", description="Traditional Valencia food")

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-name')
        serialized = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized.data)

    def test_create_recipe(self):
        payload = {
            'name': 'Spanish omelete',
            'description': 'Best food in the world'
        }

        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(name=res.data['name'])
        self.assertEqual(recipe.name, res.data['name'])

    def test_delete_recipe(self):
        recipe = Recipe.objects.create(name="Cheesecake", description="Delicious traditional cheesecake")

        recipes_delete_url = reverse('recipe:recipe-detail', kwargs={'pk': recipe.pk})
        res = self.client.delete(recipes_delete_url, data=recipe)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Recipe.objects.filter(name=recipe.name).exists()
        self.assertFalse(exists)

    def test_update_recipe(self):
        recipe = Recipe.objects.create(name="Cheesecake", description="Delicious traditional cheesecake")
        payload = {
            'name': 'New recipe',
            'description': 'A new recipe edited'
        }
        recipes_update_url = reverse('recipe:recipe-detail', kwargs={'pk': recipe.pk})
        res = self.client.patch(recipes_update_url, payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.name, payload['name'])

    def test_create_with_ingredient(self):
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [{'name': 'casa-tarradellas'}]
        }
        res = self.client.post(RECIPES_URL, payload, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.get(name=payload['name'])
        serialized = RecipeSerializer(recipes)
        self.assertEqual(res.data, serialized.data)

    #def test_update_recipe_with_details(self):


class IngredientApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.recipe = Recipe.objects.create(name="Cheesecake", description="Delicious traditional cheesecake")

    def test_retrieve_ingredients_list(self):
        Ingredient.objects.create(name='Cheese', recipe=self.recipe)
        Ingredient.objects.create(name='Milk', recipe=self.recipe)
        print(f'INGREDIENTS_URL{INGREDIENTS_URL}')
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serialized = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized.data)

    def test_create_ingredient(self):
        payload = {
            'name': 'Cheese',
            'recipe': self.recipe
        }
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ingredient = Ingredient.objects.get(name=res.data['name'])
        self.assertEqual(ingredient.name, res.data['name'])
        exists = Ingredient.objects.filter(recipe=self.recipe, name=payload['name']).exists()
        self.assertTrue(exists)

