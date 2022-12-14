from django import template
from django.utils.safestring import mark_safe
from mainApp.models import *
register = template.Library()


@register.filter(name="get_size_number")
def get_size_number(tranche,code):
    try:
        recommended_number_object = recommended_number.objects.filter(Q(tranche__id=tranche.id) & Q(size__code=code))
        return recommended_number_object[0].number
    except Exception as err:
        print(err)
        return 0

