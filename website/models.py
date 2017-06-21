from django.db import models
from sorl_cropping import ImageRatioField
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.fields import ImageField
from django.utils.html import format_html
from django.utils.timezone import now

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver


class defModel(models.Model):
    cdate = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    pdate = models.DateTimeField(verbose_name='Дата публикации', default=now)

    active = models.BooleanField(verbose_name='Активное', default=True)

    class Meta:
        abstract = True


class Lic(defModel):
    img = ImageField(verbose_name='Изображения лицензий', upload_to='lics')
    img_crop = ImageRatioField('img', '1000x1618', verbose_name='Обрезка оригинала')
    img_crop_thumbnail = ImageRatioField('img', '263x425', verbose_name='Обрезка миниатюры')

    text = models.TextField(verbose_name='Ифнормация', blank=True)
    title = models.CharField(max_length=255, verbose_name="Заголовок", blank=True)
    prior = models.IntegerField(verbose_name='приоритет порядка отображения', default=0)

    def img_admin(self):
        return format_html(
            "<a href ='%s/change/'><img src='%s' ></a>" %
            (self.id, get_thumbnail(self.img, 'x80', crop=self.img_crop).url)
        )

    class Meta:
        verbose_name = "Лицензия"
        verbose_name_plural = "Лицензии"


@receiver(post_save)
def post_save_handler(sender, **kwargs):
    cache.clear()
