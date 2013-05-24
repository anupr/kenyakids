from django import template
from django.utils.translation import ugettext_lazy

register = template.Library()

@register.simple_tag
def get_model_field_val(model, field):
    return getattr(model, "%s_en" %field, None)

@register.simple_tag
def get_model_name(model):
    return ugettext_lazy(model._meta.module_name.capitalize())
