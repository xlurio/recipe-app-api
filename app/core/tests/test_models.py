from django.test import TestCase
from django.contrib.auth import get_user_model


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
