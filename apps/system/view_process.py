from .views_system import SystemMixin
from django.views.generic.base import TemplateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
import psutil
import datetime


class ProcessContextMixin(SystemMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'process'
        return context


class ProcessListView(ProcessContextMixin, TemplateView):
    template_name = 'system/process.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '进程管理'
        context['list_type'] = self.kwargs.get('listtype')

        if context['list_type'] == 'all':
            context['process'] = psutil.process_iter(
                attrs=['pid', 'name', 'username', 'status', 'cmdline', 'memory_info', 'cpu_percent']
            )
        if context['list_type'] == 'memo':
            process = psutil.process_iter(attrs=['pid', 'name', 'username', 'status', 'cmdline', 'memory_info', 'memory_percent'])
            context['process'] = sorted(process, key=lambda process:process.info['memory_info'], reverse=True)[:100]
        if context['list_type'] == 'log':
            context['process'] = []
            for p in psutil.process_iter(['pid', 'name', 'username', 'status', 'open_files', 'cmdline']):
                for file in p.info['open_files'] or []:
                    if file.path.endswith('.log'):
                        context['process'].append(
                            {
                                'pid': p.pid, 'name': p.info['name'],'username': p.info['username'],
                                'status': p.info['status'], 'logfiles': file.path
                            }
                        )
        if context['list_type'] == 'cpu':
            process = psutil.process_iter(attrs=['pid', 'name', 'username', 'status', 'cmdline', 'cpu_percent'])
            context['process'] = sorted(process, key=lambda process:process.info['cpu_percent'], reverse=True)[:100]
        return context


class DetailView(ProcessContextMixin, TemplateView):
    template_name = 'system/process_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '进程信息'
        context['listtype'] = self.kwargs.get('listtype')
        context['breadcrumb'] = [{
            'title': '进程',
            'href': reverse_lazy('system:process:list', kwargs={'listtype': self.kwargs.get('listtype')}),
            'active': False},
            {'title': '进程详情', 'href': '', 'active': True},
        ]
        context['process'] = {}
        if psutil.pid_exists(self.kwargs.get('pid')):
            for p in psutil.process_iter():
                if p.pid == self.kwargs.get('pid'):
                    context['process']['pid'] = p.pid
                    context['process']['name'] = p.name
                    context['process']['cmdline'] = p.cmdline()
                    context['process']['username'] = p.username()
                    context['process']['cpu_percent'] = p.cpu_percent()
                    context['process']['username'] = p.username()
                    context['process']['status'] = p.status()
                    context['process']['parent'] = p.parent()
                    context['process']['tty'] = p.terminal()
                    context['process']['memory'] = p.memory_info()
                    context['process']['create_time'] = datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")
                    context['process']['files'] = []
                    for file in p.open_files():
                        context['process']['files'].append(file.path)

        return context


class ActionView(ProcessListView, RedirectView):

    # def get_redirect_url(self, *args, **kwargs):
    #     return reverse_lazy('system:process:list', kwargs={'listtype': self.kwargs.get('listtype')})

    def get(self, request, *args, **kwargs):
        pid = self.kwargs.get('pid')
        action = self.kwargs.get('action')
        if psutil.pid_exists(pid):
            if action == 'kill':
                psutil.Process(pid=pid).kill()
                messages.success(self.request, ' 标识为：' + str(pid) + ' 的进程已关闭！')
            if action == 'pause':
                psutil.Process(pid=pid).suspend()
                messages.success(self.request, ' 标识为：' + str(pid) + ' 的进程已执行暂停！')
            if action == 'resume':
                psutil.Process(pid=pid).resume()
                messages.success(self.request, ' 标识为：' + str(pid) + ' 的进程已执行恢复！')
        else:
            messages.warning(self.request, ' 标识为：' + str(pid) + ' 的进程未运行或者标识ID已经变化！不能执行！')
        return redirect(reverse('system:process:list', kwargs={'listtype': 'all'}))


