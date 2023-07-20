from django import forms
from appcommon.forms import FormBase
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError


class FirewallPortForm(FormBase):
    """ 增加防火墙端口 表单"""
    zone = forms.CharField(widget=forms.HiddenInput())
    port_type = forms.CharField(required=True)
    port_only = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    port_start = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    port_end = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    proto = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'}, choices=(('tcp', 'tcp'), ('udp', 'udp')))
    )

    def clean_port_type(self):
        data = self.cleaned_data["port_type"]
        if not data:
            raise ValidationError("必须要指定端口提交类型！")
        return data

    def clean(self):
        """ 验证字段内容 """
        cleaned_data = super().clean()
        port_type = cleaned_data.get('port_type')
        port_only = cleaned_data.get('port_only')
        port_start = cleaned_data.get('port_start')
        port_end = cleaned_data.get('port_end')
        proto = cleaned_data.get('proto')

        if (port_type == '1') and (not port_only):
            self.add_error('port_only', '端口号不能为空！')
        if (port_type == '2') and ((not port_start) or (not port_end)):
            self.add_error('port_end', '起始端口号和终止端口号必须同时存在！')

        if proto is None:
            self.add_error('proto', '必须指定端口网络协议！')


class FirewallServiceForm(FormBase):
    """ 所加防火墙允许服务 """
    zone = forms.CharField(widget=forms.HiddenInput())
    service = forms.CharField()


class ConnRenameForm(FormBase):
    """ 网络连接更名表单 """
    newname = forms.CharField(error_messages={"required": "新连接名称不能为空！"},
        required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入新名称'})
    )


class ConnForm(FormBase):
    """ 网络连接配置表单 """
    name = forms.CharField(
        label="连接名称", error_messages={"required": '连接名称不能为空！'}, required=True,
        validators=[validate_slug],
        widget=forms.TextInput(attrs={
            'class': 'form-control validate[required,custom[onlyLetterNumber],ajax[ajaxName]]',
            'data-errormessage-value-missing': '* 连接名称不能为空！',
            'data-errormessage-custom-error': '* 只能输入英文和数字!'
        })
    )
    autoconnect = forms.CharField(
        label='自动连接',
        widget=forms.CheckboxInput(
            attrs={'data-bootstrap-switch': ''}
        )
    )
    mtu = forms.IntegerField(
        label="MTU", required=False,
        widget=forms.TextInput(attrs={'class': 'form-control validate[custom[integer]]', 'placeholder': '自动'})
    )
    ipv4method = forms.CharField(
        label='IPv4模式',
        widget=forms.Select(
            choices=(('auto', '自动'), ('manual', '手动')),
            attrs={'class': 'form-control'}
        )
    )
    ip4 = forms.CharField(
        label='IPv4地址', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gw4 = forms.CharField(label='网关', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ip4dns = forms.CharField(label='DNS', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


class FileEditForm(FormBase):
    path = forms.CharField(widget=forms.HiddenInput())
    filename = forms.CharField(label='文件名',  widget=forms.TextInput(attrs={
            'class': 'validate[required]',
            'data-errormessage-value-missing': '* 文件名不能为空！',
        })
    )
    filecontent = forms.CharField(required=False, widget=forms.Textarea)


class FileDirForm(FormBase):
    path = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField(label='名称', error_messages={"required": '名称不能为空！'}, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control validate[required]',
            'data-errormessage-value-missing': '* 名称不能为空！',
        })
    )


class FileUploadForm(FormBase):
    path = forms.CharField(
        label='上传到目录：', error_messages={"required": '上传目录不能为空！'}, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control validate[required]',
            'data-errormessage-value-missing': '* 名称不能为空！',
        })
    )
    fileupload = forms.FileField(
        required=True, error_messages={"required": '上传文件不能为空！'},
        widget=forms.FileInput(attrs={
            'class': 'form-control validate[required]',
            'data-errormessage-value-missing': '* 上传文件必须要选择！',
        }))


class FileDownloadForm(FormBase):
    path = forms.CharField(widget=forms.HiddenInput)
    url = forms.CharField(
        error_messages={"required": '下载URL地址不能为空！'}, required=True,
        label='下载文件的URL', widget=forms.TextInput(attrs={
            'class': 'form-control validate[required]',
            'data-errormessage-value-missing': '* 下载URL地址不能为空！',
        })
    )