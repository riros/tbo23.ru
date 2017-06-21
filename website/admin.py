from django.contrib import admin


from sorl_cropping import ImageCroppingMixin
from sorl.thumbnail.admin.current import AdminImageMixin
from django.db import models

from website.models import Lic
from markitup.widgets import AdminMarkItUpWidget

@admin.register(Lic)
class LicAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ['id', 'pdate', 'img_admin', 'text', 'active']
    # fieldsets = (
    #     (None, {
    #         'fields': ('img', 'img_crop_thumbnail', 'img_crop')
    #     }),
    # )
    list_filter = ['active']
    ordering = ['id']
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkItUpWidget(attrs={'style': 'height: 65px;'})},
    }
    list_editable = [
        'pdate', 'text', 'active'
    ]
