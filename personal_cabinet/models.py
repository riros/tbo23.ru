from django.db.models import \
    CharField, UUIDField, Model, IntegerField, DateField, BooleanField, ManyToManyField, TextField, EmailField
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField


class Account(Model):
    name = CharField(max_length=12, primary_key=True, null=False)


class EUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not date_of_birth:
            date_of_birth = date.today()

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not date_of_birth:
            date_of_birth = date.today()

        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class EUser(AbstractUser):
    phone = PhoneNumberField(blank=True, verbose_name='Номер телефона')
    email = EmailField(_('email address'), blank=False, unique=True)
    date_of_birth = DateField(verbose_name="день рождения", null=True)
    is_admin = BooleanField(default=False, verbose_name="администратор")
    accounts = ManyToManyField(Account)
    one_c_id = UUIDField(null=False, auto_created=True, default='00000000-0000-0000-0000-000000000000')
    comment = TextField(null=True, verbose_name='Комментарий', blank=True)

    @property
    def hr_phone(self):
        return
    pass
