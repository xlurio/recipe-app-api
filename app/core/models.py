from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        # Method that creates and returns a new user
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
        # Method that creates and returns a new superuser
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.email)
