from django.db.models import \
    CharField, UUIDField, Model, IntegerField, DateField,\
    BooleanField, ManyToManyField, TextField, EmailField, ForeignKey, FloatField

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

import random


class EUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not date_of_birth:
            date_of_birth = now()

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
            date_of_birth = now()

        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class EUser(AbstractUser):
    phone = CharField(blank=True, verbose_name='Номер телефона', max_length=12)
    email = EmailField(_('email address'), blank=True, unique=True)
    date_of_birth = DateField(verbose_name="день рождения", blank=True, null=True)
    #    is_admin = BooleanField(default=False, verbose_name="администратор")
    # accounts = ManyToManyField(Account)
    # идентификатор в 1с
    alias_id = UUIDField(null=False, auto_created=True, default='00000000-0000-0000-0000-000000000000')
    comment = TextField(null=True, verbose_name='Комментарий', blank=True)
    middle_name = CharField(_('Отчество'), max_length=30, blank=True)
    # 0000-0000-0000-0000
    activation_code = CharField(_('Код активации'), max_length=20, blank=True, null=True)
    REQUIRED_FIELDS = []


    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.middle_name)
        return full_name.strip()

    pass

    @staticmethod
    def extract_phone(phone=''):
        phone = phone.replace('+7', '')
        phone = phone.replace('(', '')
        phone = phone.replace(')', '')
        phone = phone.replace('-', '')
        phone = phone.replace(' ', '')
        return phone

    @staticmethod
    def _split_name ( s='', i=0):
        # Фадеева         Лариса         Константиновна
        s = s.replace('  ', ' ')
        spl = s.split(' ')
        try:
            ret = spl[i]
        except Exception:
            ret = None
        return ret

    @classmethod
    def extract_first_name(cls, s=''):
        return cls._split_name(s, 1)

    @classmethod
    def extract_last_name(cls, s=''):
        return cls._split_name(s, 0)

    @classmethod
    def extract_middle_name(cls, s=''):
        return cls._split_name(s, 2)

    @staticmethod
    def generate_activation_code():
        return random.randrange(100000000000, 999999999999)



class Account(Model):
    name = CharField(max_length=12, primary_key=True, null=False, help_text='номер лицевого счета', verbose_name='Лицевой счет')
    ic_owner_id = UUIDField(null=False, default='00000000-0000-0000-0000-000000000000', verbose_name='код пользователя в 1с')
    address_str = TextField(null=True, blank=True, verbose_name='Адрес')
    fias_address_uuid = UUIDField(null=True, blank=True, verbose_name='Код адреса в системе fias')
    date_open = DateField(null=False, verbose_name='дата открытия')
    date_closed = DateField(null=True, help_text='если пустое значение - значит бессрочный', verbose_name='Дата закрытия', blank=True)
    message = TextField(null=True, verbose_name='сообщение пользователю', blank=True)
    euser = ForeignKey(EUser, default=1, help_text='Владелец лицевого счета', verbose_name='Владелец')

    class Meta:
        verbose_name = _('Лицевой счет')
        verbose_name_plural = _('Лицевые счета')

    @staticmethod
    def has_module_perms():
        return True

    def __str__(self):
        return self.name

    @property
    def get_balances(self):
        return MonthBalance.objects.all().filter(account=self.name).order_by('-date')


class MonthBalance(Model):
    account = ForeignKey(Account, verbose_name='Лицевой счет')
    date = DateField(verbose_name='месяц расчета')
    user_count = IntegerField('Количество проживающих', default=0)
    price = FloatField(verbose_name='суммарная цена услуг с человека', default=0)
    credit = FloatField(verbose_name='Начислено', default=0)
    payment = FloatField(verbose_name="Оплачено", default=0)
    debt = FloatField(verbose_name="Задолжность", default=0)
    discounts = ArrayField(FloatField(), null=True, blank=True, verbose_name='Скидки',
                           help_text='В рублях через запятую. Например: 20,50')

    class Meta:
        verbose_name = _('Баланс по месяцам')
        verbose_name_plural = _('Балансы по месяцам')

    def __str__(self):
        return self.account.name + self.date.strftime("/YYYY-MM")

    @property
    def d_name(self):
        return self.account.name + "/%i-%i" % (self.date.year, self.date.month)

    @property
    def short_name(self):
        return "%i-%i" % (self.date.year, self.date.month)


@receiver(pre_save, sender=EUser)
def pre_save_callback(sender=EUser,  **kwargs):
    instance = kwargs['instance']
    if not instance.activation_code:
        instance.activation_code = sender.generate_activation_code()
