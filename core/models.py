from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("User Must Have an Email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

GENDER_CHOICES = [
    ("m", "MALE"),
    ("f", "FEMALE"),
]

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=225)
    username = models.CharField(max_length=191, unique=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=191, null=True, blank=True)
    age = models.CharField(max_length=191, null=True, blank=True)
    gender = models.CharField(max_length=191, choices=GENDER_CHOICES, null=True)
    reason = models.CharField(max_length=191, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    REQUIRED_FIELDS = [
        "email",
    ]
    USERNAME_FIELD = "username"

    class Meta:
        db_table = "users"

class Quotes(models.Model):
    image_id = models.CharField(max_length=100, blank=True, null=True)
    image_uri = models.CharField(max_length=400, blank=True, null=True)
    quote = models.CharField(max_length=400, blank=True, null=True)
    auther = models.CharField(max_length=100, blank=True, null=True)
    download_uri = models.CharField(max_length=400, blank=True, null=True)
    display_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            db_table = "quotations"