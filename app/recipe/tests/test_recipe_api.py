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

    def test_create_recipe(self):
        '''Test creating recipe through recipe API'''
        payload = {
            'user': self.user,
            'title': 'Pacoca pie',
            'time_minutes': 30,
            'price': 30.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        '''Test creating recipe with tags through API'''
        tag1 = create_tag(self.user, 'Sweet')
        tag2 = create_tag(self.user, 'Pie')
        tag3 = create_tag(self.user, 'Gluten free')
        payload = {
            'user': self.user,
            'title': 'Pacoca pie',
            'time_minutes': 30,
            'price': 30.00,
            'tags': [tag1.id, tag2.id, tag3.id],
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 3)
        for tag in [tag1, tag2, tag3]:
            self.assertIn(tag, tags)

    def test_create_recipe_with_ingredients(self):
        '''Test creating recipe with ingredients through the API'''
        ingredient1 = create_ingredient(self.user, 'Pacoca')
        ingredient2 = create_ingredient(self.user, 'Milk cream')
        ingredient3 = create_ingredient(self.user, 'Butter')
        payload = {
            'user': self.user,
            'title': 'Pacoca pie',
            'time_minutes': 30,
            'price': 30.00,
            'ingredients': [ingredient1.id, ingredient2.id, ingredient3.id],
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 3)
        for ingredient in [ingredient1, ingredient2, ingredient3]:
            self.assertIn(ingredient, ingredients)

    def test_partial_update_recipe(self):
        '''Test updating some of the fields of a recipe through API'''
        recipe = create_recipe(self.user)
        recipe.tags.add(create_tag(self.user))
        new_tag = create_tag(self.user, 'Lactose free')
        payload = {
            'title': 'Milanese cheese',
            'tags': [new_tag.id, ]
        }
        url = detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertIn(new_tag, tags)

    def test_totally_update_recipe(self):
        '''Test fully updating recipe through the API'''
        recipe = create_recipe(self.user)
        recipe.tags.add(create_tag(self.user))
        new_ingredient = create_ingredient(self.user, "Carob")
        payload = {
            'user': self.user,
            'title': 'Peanut butter',
            'time_minutes': 60,
            'price': 10.00,
            'ingredients': [new_ingredient.id, ]
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload)
        recipe.refresh_from_db()
        for key in list(payload.keys())[:-1]:
            self.assertEqual(payload[key], getattr(recipe, key))
        ingredients = recipe.ingredients.all()
        tags = recipe.tags.all()
        self.assertIn(new_ingredient, ingredients)
        self.assertEqual(tags.count(), 0)
