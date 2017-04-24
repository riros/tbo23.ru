__author__ = 'riros <ivanvalenkov@gmail.com> 16.02.17'
from django.core.management.base import BaseCommand, CommandError
from personal_cabinet.models import Account, EUser, MonthBalance
from django.db import transaction
import os, json, uuid
import datetime
import transliterate

class Command(BaseCommand):
    help = "TODO"

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        for file in options['files']:
            self.stdout.write(" import '%s' ..." % file)
            if os.path.isfile(file):
                self.stdout.write(self.style.SUCCESS('файл загружен...'))

                for r in json.load(open(file)):
                    with transaction.atomic():
                        alias_id = r['owner_id']
                        euser = EUser.objects.filter(alias_id=alias_id)
                        if euser.exists():
                            #TODO вывесить сравнение пользователей
                            #euser.delete()
                            self.stdout.write('существует пользователь')
                            continue
                        else:
                            euser = EUser()
                            euser.alias_id = alias_id
                            ##self.stdout.write(r['phone'])
                            # if r['phone'] and r['phone'] > 0:
                            #     euser.phone = EUser.extract_phone(r['phone'][0])
                            euser.first_name = EUser.extract_first_name(r['owner'])
                            euser.last_name = EUser.extract_last_name(r['owner'])
                            euser.middle_name = EUser.extract_middle_name(r['owner'])
                            euser.set_password(uuid.uuid1().hex)
                            euser.is_active = False
                            #todo может дублироваться
                            euser.username = transliterate.translit(r['owner'], 'ru').replace(' ', '')
                            euser.email = str(euser.generate_activation_code()) + '@tbo23.ru'
                            euser.save()

                        acc = Account()
                        acc.name = r['n']
                        acc.address_str = r['address']
                        acc.date_open = datetime.datetime.strptime(r['date_open'], "%Y-%m-%dT%H:%M:%S.%fZ")
                        acc.date_closed = datetime.datetime.strptime(r['date_closed'], "%Y-%m-%dT%H:%M:%S.%fZ")
                        acc.message = r['message']
                        acc.euser = euser
                        acc.save()

                        for b in r['balance_history']:
                            mb = MonthBalance()
                            mb.account = acc
                            mb.date = datetime.datetime.strptime(b['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                            mb.user_count = b['user_count']
                            mb.price = b['price']
                            mb.credit = b['credit']
                            mb.payment = b['payment']
                            mb.debet = b['debet']
                            mb.save()

            else:
                self.stdout.write(self.style.ERROR("'%s' не файл!" % (file)))

