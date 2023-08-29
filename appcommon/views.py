import subprocess
import datetime
import platform
import psutil
import os

from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from .forms import LoginForm
from .forms import ShutdownForm, HostnameForm


class CosyLoginView(LoginView):
    """登录"""
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '登录'
        return context


class CosyLayoutView(LogoutView):
    """注销登录"""
    pass


class SiteHomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'home'
        context['page_title'] = '系统仪表板'
        context['os'] = subprocess.run('cat /etc/redhat-release', shell=True, capture_output=True,
                                       encoding='utf-8').stdout.strip()
        context['current_time'] = subprocess.run('date', shell=True, capture_output=True,
                                                 encoding='utf-8').stdout.strip()
        context['platform'] = platform.platform()
        context['machine'] = platform.machine()
        context['cpu'] = subprocess.run(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE, encoding="utf-8")\
            .stdout.split('\t')[6].lstrip(': ').rstrip('stepping')
        context['cpu_count'] = psutil.cpu_count()

        return context


class Shutdown(FormView):
    template_name = 'shutdown.html'
    form_class = ShutdownForm
    success_url = reverse_lazy('site_home:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'home'
        context['page_title'] = ''
        context['help_text'] = ''
        get_action = self.kwargs.get('action')
        if get_action == 'r':
            context['page_title'] = '重启'
            context['help_text'] = '<h5>注意</h5>' \
                                   '<p>提交后将执行重新启动系统。当前所有登录用户将被中断连接，所有服务将被重新启动。</p>' \
                                   '<p>将使用 shutdown -r 命令重启</p><p>重启后切勿重复提交本页！</p>'
        if get_action == 'h':
            context['page_title'] = '关机'
            context['help_text'] = '<h5>注意</h5>' \
                                   '<p>提交后将执行关闭系统。所有服务将被停止，所有用户将被中断连接，电源也会关闭(如果您的硬件支持的话)</p>' \
                                   '<p>将使用 shutdown -h 命令关机</p><p>重启后切勿重复提交本页！</p>'
        return context

    def form_valid(self, form):
        get_commander = 'shutdown -%s %s' % (self.kwargs.get('action'), form.cleaned_data['delay'])
        os.system(get_commander)
        return super().form_valid(form)


class HostnameView(FormView):
    form_class = HostnameForm
    template_name = 'hostname.html'
    success_url = reverse_lazy('site_home:index')

    def get_initial(self):
        self.initial['hostname'] = subprocess.run('hostname', shell=True, capture_output=True,
                                                  encoding="utf-8").stdout.strip("\n")
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'home'
        context['page_title'] = '配置主机名'
        context['breadcrumb'] = [
            {'title': '仪表板', 'href': reverse_lazy('site_home:index'), 'active': False},
            {'title': '配置主机名', 'href': '', 'active': True},
        ]
        return context

    def form_valid(self, form):
        hostname = form.cleaned_data['hostname']
        subprocess.run('hostnamectl set-hostname ' + hostname, shell=True, capture_output=True,
                       encoding="utf-8")
        return super().form_valid(form)