from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


ROLES = [
    ("user", "Аутентифицированный пользователь"),
    ("moderator", "Модератор"),
    ("admin", "Администратор"),
]


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        return self._create_user(
            email,
            username,
            password,
            is_superuser=True,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    confirmation_code = models.CharField(max_length=254)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        "Пользовательская роль",
        max_length=150,
        choices=ROLES,
        default="user",
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = MyUserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_user(self):
        return self.role == "user"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_admin(self):
        return self.role == "admin"

    def __str__(self):
        return self.email
