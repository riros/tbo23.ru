from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from personal_cabinet.models import *
from django.contrib.auth.models import Permission

from django.utils.html import format_html
from django.core.urlresolvers import reverse

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = EUser
        # fields = ('username', 'email', 'date_of_birth')
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EUser
        # fields = ('email', 'password', 'date_of_birth',
        #           'is_active', 'is_admin', 'one_c_id', 'phones', 'comment')
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(EUser)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'date_of_birth', 'pretty_phone', 'is_superuser', 'comment',)
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'middle_name', 'last_name', 'password', 'is_superuser')}),
        ("Контакты", {'fields': ('email', 'phone', 'comment')}),
        ('Личная информация', {'fields': ('date_of_birth',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'date_of_birth', 'password1', 'password2', 'comment')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def pretty_phone(self, euser):
        # verbose_name = _('phone')
        return '+7 %s' % euser.phone
    pretty_phone.short_description = 'Телефон'


@admin.register(MonthBalance)
class MonthBalanceAdmin(admin.ModelAdmin):
    list_display = (
        'account_link',
        'date',
        'user_count',
        'price',
        'credit',
        'payment',
    )
    list_display_links = ('date',)
    list_select_related = ('account',)
    search_fields = ('account__name',)

    def account_link(self, obj):
        return format_html('<a href="%s"> %s</a>' % (reverse('admin:%s_%s_change' % (obj._meta.app_label, obj.account._meta.model_name), args=[obj.account.name]), obj.account.name))
    account_link.short_description = "Лицевой счет"


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'euser', 'date_open', 'date_closed', 'address_str', 'fias_address_uuid',)
    list_display_links = ('name', )
    pass


# Now register the new UserAdmin...
# admin.site.register([Account, MonthBalance])
admin.site.site_header = 'Личный кабинет'
admin.site.site_title = 'ООО "Кубань ТБО"'
admin.site.index_title = 'Начало'



# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
