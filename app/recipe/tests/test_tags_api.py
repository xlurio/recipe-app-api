from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from recipe.models import Tag
from recipe.serializers import TagSerializer
from django.test import TestCase

TAGS_URL = reverse('recipe:tag-list')


class PublicTagAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test login requirement for the tags API'''
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagAPITest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='mijaro@nomuro.com',
            name='Mijaro Nomuro',
            password='senhadomijaro123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        '''Test listing user recipe tags'''
        Tag.objects.create(
            user=self.user,
            name='Italian'
        )
        Tag.objects.create(
            user=self.user,
            name='Vegan'
        )
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.order_by('-name').all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        '''Test listing logged user tags only'''
        user2 = get_user_model().objects.create_user(
            email='rolandocaio@darocha.com',
            name='Rolando Caio da Rocha',
            password='senhadorolando123'
        )
        tag = Tag.objects.create(
            user=self.user,
            name='French'
        )
        Tag.objects.create(
            user=user2,
            name='Gluten free'
        )
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag(self):
        '''Test creating a valid tag'''
        payload = {'name': 'Pasta'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
           user=self.user,
           name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_invalid_tag(self):
        '''Test creating invalid tag'''
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
