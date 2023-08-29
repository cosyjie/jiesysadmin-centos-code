import subprocess
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .views_system import SystemMixin

from .forms import TimezoneForm


class TimezoneContextMixin(SystemMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'timezone'
        return context


class TimezoneView(TimezoneContextMixin, FormView):
    template_name = 'system/timezone.html'
    form_class = TimezoneForm

    def get_initial(self):
        self.initial['set_date'] = subprocess.run('date "+%F"', shell=True, capture_output=True, encoding='utf-8').stdout.strip()
        self.initial['hour'] = subprocess.run('date "+%H"', shell=True, capture_output=True, encoding='utf-8').stdout.strip()
        self.initial['minute'] = subprocess.run('date "+%M"', shell=True, capture_output=True, encoding='utf-8').stdout.strip()
        self.initial['second'] = subprocess.run('date "+%S"', shell=True, capture_output=True, encoding='utf-8').stdout.strip()
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '时区和时间'
        cmd = 'timedatectl | grep "Time zone:"'
        context['current_zone'] = subprocess.run(
            cmd, shell=True, capture_output=True, encoding='utf-8').stdout.strip().split(': ')[1]
        cmd = 'timedatectl list-timezones'
        context['zone_list'] = subprocess.run(
            cmd, shell=True, capture_output=True, encoding='utf-8').stdout.strip().split('\n')
        context['time'] = subprocess.run('date', shell=True, capture_output=True, encoding='utf-8').stdout
        cmd = "systemctl list-unit-files | grep 'chronyd.service'"
        context['time_sync'] = subprocess.run(
            cmd, shell=True, capture_output=True, encoding='utf-8'
        ).stdout.replace('chronyd.service', '').strip()
        return context

    def get_success_url(self):
        return reverse('system:timezone:index')

    def form_valid(self, form):
        zone = form.cleaned_data.get('zone')
        time_sync = form.cleaned_data.get('time_sync')
        cmd = 'timedatectl set-timezone {}'.format(zone)
        run_end = subprocess.run(cmd, shell=True, capture_output=True, encoding='utf-8')
        if run_end.returncode != 0:
            messages.add_message(self.request, messages.warning, '设置时区异常，服务器执行信息：' + run_end.stderr)
        if time_sync == 1:
            run_end = subprocess.run(
                'systemctl start chronyd.service && systemctl enable chronyd.service',
                shell=True,capture_output=True, encoding='utf-8')
            if run_end.returncode != 0:
                messages.add_message(self.request, messages.warning, '启用同步异常，服务器执行信息：' + run_end.stderr)
        if time_sync == 2:
            run_end = subprocess.run(
                'systemctl disable chronyd.service && systemctl stop chronyd.service',
                shell=True,capture_output=True, encoding='utf-8')
            if run_end.returncode == 0:
                set_date = form.cleaned_data.get('set_date')
                hour = form.cleaned_data.get('hour')
                minute = form.cleaned_data.get('minute')
                second = form.cleaned_data.get('second')
                cmd = 'date -s "{} {}:{}:{}"'.format(set_date, hour, minute, second)
                run_end = subprocess.run(cmd, shell=True,capture_output=True, encoding='utf-8')
                if run_end.returncode != 0:
                    messages.add_message(self.request, messages.warning, '设置日期异常，服务器执行信息：' + run_end.stderr)
            else:
                messages.add_message(self.request, messages.warning, '停用同步异常，服务器执行信息：' + run_end.stderr)

        return super().form_valid(form)