from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')


class PublicUsersAPITest(TestCase):
    '''Test users API(public)'''
    test_email = 'zeca@paugordinho.com'
    test_password = 'Grf5!HwC'

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        '''Test valid user creation'''
        payload = {
            'email': self.test_email,
            'password': self.test_password,
            'name': 'Zeca Pau Gordinho'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_create_existing_user(self):
        '''Test creating user when it already exists'''
        payload = {'email': self.test_email, 'password': self.test_password}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        '''Test creating user with a too short password'''
        payload = {
            'email': self.test_email,
            'password': 'pass',
            'name': 'Zeca Pau Gordinho'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        '''Test creating a valid token'''
        payload = {
            'email': self.test_email,
            'password': self.test_password
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_invalid_credentials(self):
        '''Test creating token with invalid credentials'''
        payload = {
            'email': self.test_email,
            'password': self.test_password,
        }
        wrong_credentials = {
            'email': self.test_email,
            'password': 'wrongpass'
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, wrong_credentials)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_unexisting_user(self):
        '''Test creating token with an unexisting user'''
        res = self.client.post(TOKEN_URL, {'email': self.test_email,
                                           'password': self.test_password})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_required_fields(self):
        '''Test creating token with missing information'''
        res = self.client.post(TOKEN_URL, {'email': self.test_email,
                                           'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_managing(self):
        '''Test accessing the user management API being not credentiate'''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUsersAPITest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='tom@masturbando.com',
            password='Grf5!HwC',
            name='Tom Masturbando'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_management(self):
        '''Test correctly accessing the user management'''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
        })

    def test_post_on_management(self):
        '''Test sending HTTP POST method to user management'''
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''Test updating user profile through user management endpoint'''
        payload = {
            'name': 'Fujiro Nakombi',
            'password': 'outrasenha123'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
