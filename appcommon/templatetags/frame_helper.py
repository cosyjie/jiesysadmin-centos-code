from django import template
from django.conf import settings
from django.utils.html import format_html, mark_safe

register = template.Library()


@register.simple_tag
def get_settings(value):
    return getattr(settings, value.upper(), "")


@register.simple_tag
def html_space(value):
    return mark_safe(value.replace(' ', '&nbsp'))


@register.simple_tag
def percent(value):
    return str(round(value*100, 2)) + '%'

@register.simple_tag
def leftmenu():
    """ 获取所有菜单，其原理是获取每个apps下的对应menu.py文件内容  """
    return ''