from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import  password_validation
from utils.models import AbstractBaseModel
from utils.helpers import enforce_all_required_arguments_are_truthy
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **extra_fields):
        REQUIRED_ARGS = ("username","password")

        enforce_all_required_arguments_are_truthy(
            {
                "username": username,
                "password": password,
            },
            REQUIRED_ARGS,
        )
        username = self.model.normalize_username(username)
        #checke if user with same username already exists
        if self.model.objects.filter(username=username).exists():
            raise ValueError('A user with this username already exists')
        #validate password
        # ensure that the passwords are strong enough.
        try:
            password_validation.validate_password(password)
        except ValidationError as exc:
            # return error accessible in the appropriate field, ie password
            raise ValidationError({"password": exc.messages}) from exc
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseModel,AbstractUser):
    username = models.CharField(max_length=150, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.username
