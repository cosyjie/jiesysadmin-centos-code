from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError

class FormBase(forms.Form):
    """
    基础表单 不使用表单生成HTML5验证
    """
    use_required_attribute = False


class LoginForm(AuthenticationForm, FormBase):
    """登录表单"""
    username = UsernameField(
        error_messages={'required': '请输入登录用户名！'},
        widget=forms.TextInput(
            attrs={'autofocus': True, 'class': 'form-control validate[required]', 'autocomplete': 'username',
                   'placeholder': '用户名', 'data-errormessage-value-missing': '请输入用户名！'}
        )
    )
    password = forms.CharField(
        error_messages={'required': '请输入登录密码！'},
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-control validate[required]', 'placeholder': '密码',
                                          'data-errormessage-value-missing': '请输入密码！'}
                                   ),
    )


class HostnameForm(FormBase):
    """ 修改当前主机名表单 """
    hostname = forms.CharField(label="主机名", widget=forms.TextInput(
        attrs={'class': 'form-control validate[required]'}
    ))

    def clean_hostname(self):
        data = self.cleaned_data['hostname']
        if not data:
            raise ValidationError("必须要指定主机名称！")
        return data


class ShutdownForm(FormBase):
    delay = forms.ChoiceField(
        label="延迟时间",
        choices=(('now', '立即'), ('1', '1分钟'), ('5', '5分钟'), ('20', '20分钟'), ('40', '40分钟'), ('60', '60分钟')),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
