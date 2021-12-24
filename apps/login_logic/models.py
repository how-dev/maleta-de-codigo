from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(email, password, **extra_fields)


class FinalUserModel(AbstractUser):
    username = None
    user_permissions = None
    first_name = None
    last_name = None
    groups = None
    is_superuser = None
    is_staff = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    objects = UserManager()

    class Meta:
        db_table = 'user"."final_user'
        managed = True
