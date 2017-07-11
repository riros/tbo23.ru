__author__ = 'riros <ivanvalenkov@gmail.com> 16.02.17'
from django.core.management.base import BaseCommand, CommandError
from cabinet.models import Account, EUser, MonthBalance
from django.db import transaction
import os, json, uuid, sys
import datetime
import transliterate
from phonenumbers.phonenumberutil import NumberParseException

import phonenumbers
import re


class Command(BaseCommand):
    help = "TODO"

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        for file in options['files']:
            self.stdout.write(" import '%s' ..." % file)
            if os.path.isfile(file):
                self.stdout.write(self.style.SUCCESS('файл загружен...'))

                inactive_users = EUser.objects.filter(is_staff=False).delete()

                for r in json.load(open(file)):
                    n = r['n']
                    sys.stdout.write('%s    \b\r' % n)
                    with transaction.atomic():
                        alias_id = r['owner_id']
                        uname = transliterate.translit(r['owner'], 'ru').replace(' ', '')
                        euser = EUser.objects.filter(alias_id=alias_id)
                        if euser.exists():
                            # TODO вывесить сравнение пользователей
                            # euser.delete()
                            # self.stdout.write('пропускаем %s' % alias_id)
                            euser = euser.get()
                        else:
                            saved = False
                            i = 0
                            while i < 10 and not saved:
                                i = i + 1
                                euser = EUser.objects.filter(username=uname)
                                if euser.exists():
                                    uname = '%s_%s' % (uname, i)
                                    self.stdout.write('Дубль пользователя по имени переименовываем на %s' % uname)
                                    saved = False
                                else:
                                    saved = True

                            if not saved:
                                self.stderr.write(
                                    "Ошибка поиска алтернативного имени для пользователя %s \n" % uname)
                                continue
                            else:
                                euser = EUser()
                            euser.alias_id = alias_id
                            euser.set_password(uuid.uuid1().hex)
                            euser.is_active = True
                            euser.email = str(euser.generate_activation_code()) + '@tbo23.ru'

                        euser.first_name = EUser.extract_first_name(r['owner'])
                        euser.last_name = EUser.extract_last_name(r['owner'])
                        euser.middle_name = EUser.extract_middle_name(r['owner'])
                        euser.username = uname

                        if r['phone'] and len(r['phone']) > 0:
                            sph = r['phone'][0]
                            try:
                                if sph != 'нет':
                                    ph = phonenumbers.parse(sph)
                                else:
                                    ph = None
                                euser.phone = ph
                            except NumberParseException:
                                m = re.match('\+?7?8?[^\d|^-]*([\d]+)[^\d|^-]*([\d|\-]*)', sph)
                                if m:
                                    sph = '+7'
                                    for g in m.groups():
                                        sph = sph + g
                                else:
                                    ph = None
                                try:
                                    ph = phonenumbers.parse(sph)
                                    euser.phone = ph
                                except NumberParseException:
                                    self.stderr.write(
                                        'Ошибка формата телефона: "%s",  пользователь: %s %s \n' % (
                                            sph, euser.get_full_name(), euser.alias_id))
                        # try:
                        euser.save()
                        # except:
                        #     self.stderr.write(
                        #         "Ошибка сохранения пользователя, %s %s \n" % (euser.get_full_name(), euser.alias_id))


                        acc = Account.objects.filter(name=n)
                        try:
                            if acc.exists():
                                self.stdout.write('Перезапись лицевого %s' % n)
                                acc = acc.get()
                            else:
                                acc = Account()
                                acc.name = r['n']
                        except:
                            self.stderr.write('ошибка выборки лицевого счета %s %s' % (n, acc))

                        acc.address_str = r['address']
                        acc.date_open = datetime.datetime.strptime(r['date_open'], "%Y-%m-%dT%H:%M:%S.%fZ")
                        acc.date_closed = datetime.datetime.strptime(r['date_closed'], "%Y-%m-%dT%H:%M:%S.%fZ")
                        acc.message = r['message']
                        acc.euser = euser
                        try:
                            acc.save()
                        except:
                            self.stderr.write('Ошбика сохранения лицевого счета ', n, acc)
                            break

                        for b in r['balance_history']:
                            pydate = datetime.datetime.strptime(b['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                            mb = MonthBalance.objects.filter(account=acc, date=pydate)
                            if mb.exists():
                                self.stdout.write("перезапись баланса %s %s \n" % (mb.account.name, pydate))
                                mb = mb.get()
                            else:
                                mb = MonthBalance()
                                mb.account = acc
                                mb.date = pydate
                            mb.user_count = b['user_count']
                            mb.price = b['price']
                            mb.credit = b['credit']
                            mb.payment = b['payment']
                            # mb.debet = b['debet']
                            mb.debet = mb.credit - mb.payment
                            mb.save()
            else:
                self.stdout.write(self.style.ERROR("'%s' не файл!" % (file)))
