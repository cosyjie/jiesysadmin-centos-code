from django import forms
from appcommon.forms import FormBase


class PythonInstallForm(FormBase):
    version = forms.CharField(label='可选版本', required=True)
    # website = forms.CharField(
    #     label='下载源', required=True,
    #     widget=(forms.Select(attrs={'class': 'form-control validate[required]'},
    #         choices=(('huaweicloud', '华为云'), ('python', 'Python官方(可能较慢)'))
    #     )
    #     )
    # )
