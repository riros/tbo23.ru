from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'siteindex/index.html', context={
        # 'accounts': Account.objects.all().filter(euser=request.user)

    })

def source(request):
    return render(request, 'smoothy_source.html', context={
    })
