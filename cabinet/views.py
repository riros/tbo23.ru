from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_page
from django.http.response import HttpResponse

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.http import is_safe_url, urlsafe_base64_decode

from django.utils.decorators import method_decorator

from django.http import HttpResponseRedirect

from django.views.generic.edit import FormView
from .models import *
from .forms import AuthenticationForm
from project import settings

from django.urls import NoReverseMatch, reverse

SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'


# REDIRECT_FIELD_NAME = 'next'


# @cache_page(60 * 15)
@login_required(login_url='/cabinet/login/')
def user_account_page(request, acc_id):
    return render(request, 'personal_cabinet/index.html', context={'acc_id': acc_id})


@login_required(login_url='/cabinet/login/')
def index(request):
    return render(request, 'personal_cabinet/index.html', context={
        'DEBUG': settings.DEBUG,
        'user': request.user,
        'accounts': Account.objects.filter(euser=request.user)
    })


class SuccessURLAllowedHostsMixin(object):
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        allowed_hosts = {self.request.get_host()}
        allowed_hosts.update(self.success_url_allowed_hosts)
        return allowed_hosts


class LoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Displays the login form and handles the login action.
    """
    form_class = AuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    # template_name = 'personal_cabinet/login.html'
    template_name = 'personal_cabinet/login-2.html'

    redirect_authenticated_user = True
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Ensure the user-originating redirection URL is safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        if not url_is_safe:
            return resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_success_url(),
            'site': current_site,
            'site_name': current_site.name,
            'DEBUG': settings.DEBUG,
            'site_header': 'Авторизация в личном кабенете'
        })
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context


@never_cache
def logout(req):
    auth_logout(req)
    return HttpResponseRedirect('/')

# @login_required()
# def load_users(req):
#     if req.user.is_authenticated:
#         return render(req, 'personal_cabinet/ok.html')
#     else:
#         return render(req, 'personal_cabinet/error.html')
