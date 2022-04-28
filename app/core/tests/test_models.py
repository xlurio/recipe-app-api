from django.contrib.auth import get_user_model
from core.models import Ingredient, Recipe, Tag
from django.test import TestCase


def sample_user():
    email = 'kagaro@nakama.com'
    name = 'Kagaro Nakama'
    password = 'senhadokagaro123'
    return get_user_model().objects.create_user(
        email=email,
        name=name,
        password=password
    )


# Write your tests here
class ModelTests(TestCase):
    test_password = 'Grf5!HwC'
    test_email = 'test@calegario.com'

    def test_create_user(self):
        """Test user creation"""
        user = get_user_model().objects.create_user(
            email=self.test_email,
            password=self.test_password
        )
        self.assertEqual(user.email, self.test_email)
        self.assertTrue(user.check_password(self.test_password))

    def test_normalize_email(self):
        """Test email normalizing"""
        email = 'test@CALEGARIO.com'
        user = get_user_model().objects.create_user(
            email=email,
            password=self.test_password
        )
        self.assertEqual(user.email, self.test_email)

    def test_create_user_wo_email(self):
        """Test user creation without email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password=self.test_password
            )

    def test_create_superuser(self):
        """Test superuser creation"""
        user = get_user_model().objects.create_superuser(
            email=self.test_email,
            password=self.test_password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_tag(self):
        '''Test recipe tag creation'''
        tag = Tag.objects.create(
            user=sample_user(),
            name='Italian'
        )
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        '''Test ingredient creation'''
        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Shitake'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_create_recipe(self):
        '''Test recipe creation'''
        recipe = Recipe.objects.create(
            user=sample_user(),
            title='hearts of palm risotto',
            time_minutes=30,
            price=50.00
        )
        self.assertEqual(str(recipe), recipe.title)
