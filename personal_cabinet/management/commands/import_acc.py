__author__ = 'riros <ivanvalenkov@gmail.com> 16.02.17'
from django.core.management.base import BaseCommand, CommandError

from personal_cabinet.models import Account, EUser, MonthBalance
import os, json


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
                    self.stdout.write('__________________')

                    alias_id = r['owner_id']
                    euser = EUser.objects.filter(alias_id=alias_id)
                    if euser.exists():
                        euser.delete()
                        self.stdout.write('существует удаляю')
                    else:
                        euser = EUser()
                        euser.alias_id = alias_id
                        euser.phone = EUser.extract_phone(r['phone'])
                        euser.first_name = EUser.extract_first_name(r['owner'])
                        euser.last_name = EUser.extract_last_name(r['owner'])
                        euser.middle_name = EUser.extract_middle_name(r['owner'])
                        euser.set_password('KKedjjdlLLehh23s')
                        euser.is_active = False
                        euser.save()
                    break

            else:
                self.stdout.write(self.style.ERROR("'%s' не файл!" % (file)))

