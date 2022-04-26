from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import Ingredient
from recipe.serializers import IngredientSerializer
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientAPITests(TestCase):
    '''Test the publicly available ingredients API'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test access ingredient API without been logged'''
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):
    '''Test the private ingredient API'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='exodia@silva.com',
            password='senhadoexodia123',
            name='Exodia Silva'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_ingredients(self):
        '''Test listing ingredients'''
        Ingredient.objects.create(
            user=self.user,
            name='Heart of palm'
        )
        Ingredient.objects.create(
            user=self.user,
            name='Rice'
        )

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        '''Test the ingredients are limited to the user ingredients'''
        user2 = get_user_model().objects.create_user(
            email='peter@parker.com',
            password='senhadopeter123',
            name='Peter Parker'
        )
        Ingredient.objects.create(
            user=user2,
            name='Asparagus'
        )
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Penne'
        )
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient(self):
        '''Test creating ingredient'''
        payload = {'name': 'Eggs'}
        self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists
        self.assertTrue(exists)

    def test_invalid_ingredient(self):
        '''Test posting invalid ingredient'''
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
