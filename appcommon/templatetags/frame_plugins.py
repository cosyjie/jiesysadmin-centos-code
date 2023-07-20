from django import template
from django.conf import settings
from django.utils.html import format_html, mark_safe

register = template.Library()

plugin_dir = settings.STATIC_URL + 'plugins/'

template_file_css = '<link rel="stylesheet" href="{}" />'
template_file_js = '<script src="{}"></script>'


@register.simple_tag
def jquery_validate_assets():
    """Jquery validate 插件的 javascript 文件"""
    this_dir = 'jquery-validation/'
    return format_html(
        template_file_js + template_file_js + template_file_js,
        plugin_dir + this_dir + 'jquery.validate.min.js',
        plugin_dir + this_dir + 'additional-methods.min.js',
        plugin_dir + this_dir + 'localization/messages_zh.min.js',
    )


@register.simple_tag
def jquery_validation_engine(file_type, **kwargs):
    """ jquery_validation_engine 验证插件的文件 """
    this_dir = 'jquery-validation-engine/'
    if file_type == 'css':
        return format_html(template_file_css, plugin_dir + this_dir + 'validationEngine.jquery.css')
    if file_type == 'js':
        return format_html(
            template_file_js + template_file_js + template_file_js,
            plugin_dir + this_dir + 'jquery.validationEngine-zh_CN.js',
            plugin_dir + this_dir + 'other-validations.js',
            plugin_dir + this_dir + 'jquery.validationEngine.min.js',
        )
    if file_type == 'jscode':
        return format_html('$("#{}")', kwargs['form_id']) + \
            mark_safe('.validationEngine({ "promptPosition": "bottomLeft", "isError":"false"});')


@register.simple_tag
def jquery_confirm(file_type, **kwargs):
    """ jquery confirm 插件配置 """
    this_dir = 'jquery-confirm/'
    if file_type == 'css':
        return format_html(template_file_css, plugin_dir + this_dir + 'jquery-confirm.css')
    if file_type == 'js':
        return format_html(template_file_js, plugin_dir + this_dir + 'jquery-confirm.js')


@register.simple_tag
def toastr(file_type):
    """ jquery toastr 提示插件配置 """
    this_dir = 'toastr/'
    if file_type == 'css':
        return format_html(template_file_css, plugin_dir + this_dir + 'toastr.min.css')
    if file_type == 'js':
        return format_html(template_file_js, plugin_dir + this_dir + 'toastr.min.js')


@register.simple_tag
def select2(file_type):
    """ jquery select2 下拉插件 """
    this_dir = 'select2/'
    if file_type == 'css':
        return format_html(template_file_css, plugin_dir + this_dir + 'css/select2.min.css')
    if file_type == 'js':
        return format_html(template_file_js, plugin_dir + this_dir + 'js/select2.min.js')
    if file_type == 'jscode':
        return mark_safe("$('.select2').select2();")


@register.simple_tag
def bootstrap_switch():
    """ bootstrap switch 复选框插件文件调用"""

    this_dir = 'bootstrap-switch/'
    return format_html(
        template_file_js,
        plugin_dir + this_dir + 'js/bootstrap-switch.min.js'
    )


@register.simple_tag
def codemirror(file_type, id_element=''):
    this_dir = 'codemirror/'
    # mode = ''
    # mode_file = ''
    # if ext == 'py':
    #     mode = 'python'
    #     mode_file = 'python/python.js'
    # if ext == 'js':
    #     mode = 'javascript'
    #     mode_file = 'javascript/javascript.js'
    # if ext == 'css':
    #     mode = 'css'
    #     mode_file = 'css/css.js'
    # if ext == 'xml':
    #     mode = 'xml'
    #     mode_file = 'xml/xml.js'
    # if ext == 'html' or ext == 'htm':
    #     mode = 'html'
    #     mode_file = 'htmlmixed/htmlmixed.js'
    # if ext == 'sh':
    #     mode = 'sh'
    #     mode_file = 'shell/shell.js'
    # if ext == 'php':
    #     mode = 'php'
    #     mode_file = 'php/php.js'
    # if ext == 'go':
    #     mode = 'go'
    #     mode_file = 'go/go.js'

    if file_type == 'css':
        return format_html(
            template_file_css + template_file_css,
            plugin_dir + this_dir + 'lib/codemirror.css',
            plugin_dir + this_dir + 'theme/monokai.css'
        )
    if file_type == 'js':
        return format_html(
            template_file_js + template_file_js + template_file_js,
            plugin_dir + this_dir + 'lib/codemirror.js',
            plugin_dir + this_dir + 'addon/mode/loadmode.js',
            plugin_dir + this_dir + 'mode/meta.js',

        )

