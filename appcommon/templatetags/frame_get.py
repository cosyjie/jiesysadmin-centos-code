from django import template
import socket

register = template.Library()


@register.simple_tag
def get_hostname():
    return socket.gethostname()

