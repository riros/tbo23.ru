from django.shortcuts import render

from django.views.decorators.cache import cache_page

from website.models import Lic
from project import settings


# Create your views here.

# @cache_page(60 * 60 * 24 * 30 * 12)
def index(request):
    lics = Lic.objects.filter(active=True).order_by('-prior')

    return render(request, 'index.html', context={
        'DEBUG': settings.DEBUG,
        'lics': lics
        # 'accounts': Account.objects.all().filter(euser=request.user)

    })

