import os
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.conf import settings


def recipe_image_file_path(instance, filename):
    '''Returns the final path of the uploaded image'''
    extension = str(filename).split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join('uploads/recipe', filename)


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        '''Method that creates and returns a new user'''
        if not email:
            raise ValueError('An email must be set')
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        '''Method that creates and returns a new superuser'''
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ''' User model'''
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.email)


class Tag(models.Model):
    '''Model of the recipe tags'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Model for the ingredients'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Model for the recipes'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
