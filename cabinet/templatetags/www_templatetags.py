__author__ = 'riros <ivanvalenkov@gmail.com> 02.06.17'
from django import template
from math import fabs
register = template.Library()


@register.filter()
def abs(val):
    return fabs(float(val))
