from django.db.models import CharField, UUIDField, Model, IntegerField
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Account(Model):
    name = CharField(max_length=12, primary_key=True, null=False)
    owner = CharField(max_length=255, null=False)
    owner_id = UUIDField(null=False)
    phones = ArrayField(IntegerField())
