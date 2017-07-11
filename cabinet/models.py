from django.db.models import \
    CharField, UUIDField, Model, IntegerField, DateField, \
    BooleanField, ManyToManyField, TextField, EmailField, \
    ForeignKey, FloatField, OneToOneRel

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
import random

from django.utils.dateformat import format


class defModel(models.Model):
    cdate = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    active = models.BooleanField(verbose_name='Активное', default=True)

    class Meta:
        abstract = True


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
        print("heee")
        if not email:
            email = 'it@tbo23.ru'
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
    phone = PhoneNumberField(null=True, blank=True, verbose_name='Номер телефона')
    email = EmailField(_('email address'), blank=True, unique=True)
    date_of_birth = DateField(verbose_name="день рождения", blank=True, null=True)
    #    is_admin = BooleanField(default=False, verbose_name="администратор")
    # accounts = ManyToManyField(Account)
    # идентификатор в 1с
    alias_id = UUIDField(null=False, auto_created=True, default='00000000-0000-0000-0000-000000000000')
    comment = TextField(null=True, verbose_name='Комментарий', blank=True)
    middle_name = CharField(_('Отчество'), max_length=30, blank=True, null=True)
    # 0000-0000-0000-0000
    activation_code = CharField(_('Код активации'), max_length=20, blank=True, null=True)

    # REQUIRED_FIELDS = []
    @staticmethod
    def get_accounts(euser):
        return Account.objects.filter(euser=euser, active=True)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.middle_name)
        return full_name.strip()

    pass

    # @staticmethod

    # def extract_phone(phone=''):
    #     # todo
    #     return phone.replace('+7', '') \
    #         .replace('+7', '') \
    #         .replace('(', '') \
    #         .replace('(', '') \
    #         .replace('-', '') \
    #         .replace(' ', '')

    @staticmethod
    def _split_name(s='', i=0):
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


class Organization(defModel):
    name = CharField(max_length=255, null=False, help_text='Название организации',
                     verbose_name='Организация', default='ООО "Кубань-ТБО"')

    def __str__(self):
        return self.name


class Account(defModel):
    _balance_cache = None
    name = CharField(max_length=12, null=False, help_text='номер лицевого счета',
                     verbose_name='Лицевой счет')
    # ic_owner_id = UUIDField(null=False, default='00000000-0000-0000-0000-000000000000', verbose_name='код пользователя в 1с')
    address_str = TextField(null=True, blank=True, verbose_name='Адрес')
    fias_address_uuid = UUIDField(null=True, blank=True, verbose_name='Код адреса в системе fias')
    date_open = DateField(null=False, verbose_name='дата открытия')
    date_closed = DateField(null=True, help_text='если пустое значение - значит бессрочный',
                            verbose_name='Дата закрытия', blank=True)
    message = TextField(null=True, verbose_name='сообщение пользователю', blank=True)
    euser = ForeignKey(EUser, default=1, help_text='Владелец лицевого счета',
                       verbose_name='Владелец', on_delete=models.CASCADE)
    organization = ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация", default=1)

    # balances = OneToOneRel('date', MonthBalance, 'account')

    class Meta:
        verbose_name = _('Лицевой счет')
        verbose_name_plural = _('Лицевые счета')

    def get_balance(self, accurate=2):
        mbs = MonthBalance.objects.filter(active=True, account=self).order_by('date')
        ret = 0
        for mb in mbs:
            ret = ret - mb.debet
        return round(ret, accurate)

    @staticmethod
    def has_module_perms():
        return True

    def __str__(self):
        return self.name

    @property
    def get_balances(self):
        return MonthBalance.objects.filter(account=self).order_by('-date')

    @property
    def balances_count(self):
        return self.get_balances.count()

    @staticmethod
    def find_user_from_afio(a, f, i, o):
        q = Account.objects.filter(name__iexact=a, active=True, euser__first_name__iexact=i, euser__last_name__iexact=f,
                                   euser__middle_name__iexact=o)

        return q.get().euser if q.exists() else None


class MonthBalance(defModel):
    account = ForeignKey(Account, verbose_name='Лицевой счет')
    date = DateField(verbose_name='месяц расчета')
    user_count = IntegerField('Количество проживающих', default=0)
    price = FloatField(verbose_name='суммарная цена услуг с человека', default=0)
    credit = FloatField(verbose_name='Начислено', default=0)
    payment = FloatField(verbose_name="Оплачено", default=0)
    debet = FloatField(verbose_name="Задолжность", default=0)
    # discounts = ArrayField(FloatField(), null=True, blank=True, verbose_name='Скидки',
    #                        help_text='В рублях через запятую. Например: 20,50')
    discount = FloatField(null=True, blank=True, verbose_name="Скидка")

    class Meta:
        verbose_name = _('Баланс по месяцам')
        verbose_name_plural = _('Балансы по месяцам')

    def __str__(self):
        return "%s-%s г." % ( self.date.month,  self.date.year)

    @property
    def d_name(self):
        return self.account.name + "/%i-%i" % (self.date.year, self.date.month)


@receiver(pre_save, sender=EUser)
def pre_save_callback(sender=EUser, **kwargs):
    instance = kwargs['instance']
    if not instance.activation_code:
        instance.activation_code = sender.generate_activation_code()
