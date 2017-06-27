__author__ = 'riros <ivanvalenkov@gmail.com> 22.06.17'
from django import forms
import unicodedata
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.text import capfirst

UserModel = get_user_model()


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    accountname = UsernameField(
        label='Лицевой счет',
        max_length=20,
        widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}),
    )

    f = UsernameField(
        label='Фамилия',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    i = UsernameField(
        label='Имя',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    o = UsernameField(
        label='Отчество',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )

    # password = forms.CharField(
    #     label=_("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    # )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        # self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        # if self.fields['accountname'].label is None:
        #     self.fields['accountname'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
