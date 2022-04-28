from rest_framework.test import APIClient
from django.test import TestCase
from recipe.serializers import (
    DetailSerializer, RecipeSerializer
)
from django.contrib.auth import get_user_model
from core.models import Ingredient, Recipe, Tag
from django.urls import reverse
from rest_framework import status

RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    '''Function that returns the url of the recipe details endpoint'''
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_ingredient(user, name='Sugar'):
    '''Function that creates and returns a new ingredient'''
    return Ingredient.objects.create(
        user=user,
        name=name
    )


def create_recipe(user, **kwargs):
    '''Function that creates and returns a new recipe'''
    recipe_data = {
        'user': user,
        'title': 'Sample recipe',
        'time_minutes': 60,
        'price': 30.00,
    }
    recipe_data.update(kwargs)
    return Recipe.objects.create(**recipe_data)


def create_tag(user, name='bakery'):
    '''Function that creates and returns a new tag'''
    return Tag.objects.create(
        user=user,
        name=name
    )


class PublicRecipeAPITests(TestCase):
    '''Test publicly available recipe API features'''

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_access(self):
        '''Test accessing API without been credentiated'''
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    '''Test private recipe API'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='he@man.com',
            password='senhadohe123',
            name='He Man'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        '''Test listing recipes for the authenticated user'''
        create_recipe(self.user)
        create_recipe(
            user=self.user,
            title='Lasagna',
            time_minutes=30,
            price=30.00
        )
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_user_only_recipes(self):
        '''Test if the API shows recipes other than the ones from the
        authenticated user'''
        user2 = get_user_model().objects.create_user(
            email='tom@jobin.com',
            password='senhadotom123',
            name='Tom Jobin'
        )
        create_recipe(self.user)
        create_recipe(
            user=user2,
            title='Cheese conchiglione',
            time_minutes=25,
            price=20.50
        )
        recipes = Recipe.objects.all().filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_details(self):
        '''Test retrieving details from a recipe'''
        recipe = create_recipe(self.user)
        recipe.tags.add(create_tag(self.user))
        recipe.ingredients.add(create_ingredient(self.user))
        serializer = DetailSerializer(recipe)
        res = self.client.get(detail_url(recipe.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
