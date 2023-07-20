from importlib import import_module
from django import template
from django.urls import reverse
from django.conf import settings
from django.utils.html import format_html, mark_safe

register = template.Library()


@register.simple_tag
def menu(parent_menu, submenu):
    menus = {}
    html = ''
    for app in settings.INSTALLED_APPS:
        if app[:5] == 'apps.':
            append_list = import_module(app + '.menu')
            menu_list = append_list.menu
            for k, v in menu_list.items():
                if k in menus:
                    if v['child']:
                        for child in v['child']:
                            if child not in menus[k]['child']:
                                menus[k]['child'].append(child)
                else:
                    menus[k] = v

    for k, value in menus.items():
        html += '<li class="nav-item'
        if parent_menu == k:
            html += ' menu-open'
        html += '"><a href="#" class="nav-link'
        if parent_menu == k:
            html += ' active'
        html += '"><i class="nav-icon ' + value['ico'] + '"></i><p>' + value['title'] + \
                '<i class="right fas fa-angle-left"></i></p></a>'
        if value['child']:
            html += '<ul class="nav nav-treeview">'
            for sub in value['child']:
                html += '<li class="nav-item"><a href="' + sub['href'] + '" class="nav-link'
                if parent_menu == k and submenu == sub['name']:
                    html += ' active'
                html += '"><i class="far fa-circle nav-icon"></i><p>' + sub['title'] +'</p></a></li>'
            html += '</ul>'
        html += '</li>'

    return mark_safe(html)


@register.simple_tag
def form_btn(*args, **kwargs):
    html = ''
    if 'submit' in args:
        html += ' <button type="submit" class="btn btn-info margin_right_5" id="form_btn_submit" name="form_btn_submit">提交</button>'
    if 'back' in args:
        html += ' <button type="button" class="btn btn-default float-right margin_right_5" id="form_btn_back" ' \
                'name="form_btn_back" onclick="javascript:history.back();">返回</button> '
    if 'reset' in args:
        html += ' <button type="reset" class="btn btn-secondary float-right margin_right_5" id="form_btn_reset" ' \
                'name="form_btn_reset">重置</button> '
    if 'search' in args:
        html += ' <button type="button" class="btn btn-primary margin_right_5" id="search_form_btn_search">' \
                '<i class="fa fa-search"></i> 查询</button>'

    return mark_safe(html)


@register.simple_tag
def link_btn(*args, **kwargs):
    html = ''
    if 'create' in args:
        if 'url_args' not in kwargs.keys():
            kwargs['url_args'] = []

        html += '<a class="btn btn-outline-success margin_right_10" href="' + reverse(kwargs['url'], args=kwargs['url_args']) + '">' \
                + '<i class="fa fa-plus"></i> ' + kwargs['text'] + '</a>'

    return mark_safe(html)
