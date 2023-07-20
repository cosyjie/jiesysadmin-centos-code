import os
import subprocess
from xml.dom.minidom import parse

from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView
from django.contrib import messages

from .views_system import SystemMixin

from .forms import FirewallPortForm, FirewallServiceForm


def get_firewalld_state():
    """ 获取防火墙当前状态 """
    firewall_state = subprocess.run('firewall-cmd --state', shell=True, capture_output=True, encoding="utf-8")
    if firewall_state.stderr.strip("\n") == "not running":
        return False
    if firewall_state.stdout.strip("\n") == "running":
        return True


def firewalld_reload():
    """ 刷新防火墙规则 """
    os.system('firewall-cmd --reload')


def system_services():
    """ 获取服务列表 """

    """ 读取所有预置服务 """
    service_list = {}
    service_path = '/usr/lib/firewalld/services/'
    service_files = os.listdir(service_path)
    for filename in service_files:
        dom = parse(service_path + filename)
        port_udp = []
        port_tcp = []
        root = dom.documentElement
        get_short = root.getElementsByTagName('short')
        name = short = filename.replace('.xml', '')
        if len(get_short):
            short = get_short[0].firstChild.data

        ports = root.getElementsByTagName('port')
        for item in ports:
            protocol = item.getAttribute('protocol')
            port = item.getAttribute('port')
            if protocol == 'tcp':
                port_tcp.append(port)
            if protocol == 'udp':
                port_udp.append(port)
        service_list[name] = {'short': short, 'udp': port_udp, 'tcp': port_tcp}

    """ 读取可能存在的追加服务 """
    service_path = '/etc/firewalld/services/'
    service_files = os.listdir(service_path)
    for filename in service_files:
        dom = parse(service_path + filename)
        port_udp = []
        port_tcp = []
        root = dom.documentElement
        get_short = root.getElementsByTagName('short')
        name = short = filename.replace('.xml', '')
        if len(get_short):
            short = get_short[0].firstChild.data

        ports = root.getElementsByTagName('port')
        for item in ports:
            protocol = item.getAttribute('protocol')
            port = item.getAttribute('port')
            if protocol == 'tcp':
                port_tcp.append(port)
            if protocol == 'udp':
                port_udp.append(port)
        service_list[name] = {'short': short, 'udp': port_udp, 'tcp': port_tcp}

    return service_list


class FirewallMixin(SystemMixin):
    """ 防火墙栏目基础参数 """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'firewalld'
        return context


class FirewalldGetZoneMixin(FirewallMixin):
    """ 防火墙 区域列表参数 """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zones'] = subprocess.run(
            'firewall-cmd --get-zones', shell=True, capture_output=True, encoding="utf-8"
        ).stdout.strip('\n').split(' ')
        context['defaultZone'] = subprocess.run(
            'firewall-cmd --get-default-zone', shell=True, capture_output=True, encoding="utf-8"
        ).stdout.split(' ')[0].strip('\n')
        context['currentZone'] = context['defaultZone']
        zone = self.request.GET.get('zone')
        if zone:
            context['currentZone'] = zone
        return context


class FirewalldView(FirewallMixin, TemplateView):
    """ 防火墙首页  """
    template_name = 'system/firewalld.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '防火墙'
        firewall_state = subprocess.run('systemctl status firewalld', shell=True, capture_output=True,
                                        encoding="utf-8").stdout.split('\n')[:3]
        context['service'] = firewall_state[0].strip('● ').strip()
        context['loaded'] = firewall_state[1].replace('Loaded: loaded (', '').replace(')', '').split(';')[0]
        context['statue'] = firewall_state[2].split(' since ')[0].replace('Active: ', '')
        context['boot'] = subprocess.run('systemctl is-enabled firewalld', shell=True, capture_output=True,
                                       encoding="utf-8").stdout.strip("\n")
        context['statue_str'] = 'no' if 'inactive' in context['statue'] else 'yes'
        context['defaultZone'] = subprocess.run('firewall-cmd --get-default-zone',
                                                shell=True, capture_output=True,
                                                encoding="utf-8").stdout.split(' ')[0].strip('\n')
        return context


class FirewalldActionView(FirewallMixin, RedirectView):
    """ 防火墙操作 """
    url = reverse_lazy('system:firewalld:index')

    def get(self, request, *args, **kwargs):
        action = self.request.GET.get('action')
        if action == 'start':  os.system('systemctl start firewalld')
        if action == 'stop':  os.system('systemctl stop firewalld')
        if action == 'restart':  os.system('systemctl restart firewalld')
        if action == 'reload':  firewalld_reload()
        if action == 'disabled':  os.system('systemctl disable firewalld')
        if action == 'enabled':  os.system('systemctl enable firewalld')

        return super().get(request, *args, **kwargs)


class FirewalldReloadView(RedirectView):
    """ 重载防火墙规则 """

    def get_redirect_url(self, *args, **kwargs):
        page = self.request.GET.get('from')
        zone = self.request.GET.get('zone')
        if page == 'port':
            return reverse('system:firewalld:port') + '?zone=' + zone
        if page == 'service':
            return reverse('system:firewalld:service') + '?zone=' + zone

    def get(self, request, *args, **kwargs):
        firewalld_reload()
        return super().get(request, *args, **kwargs)


class FirewalldPortView(FirewalldGetZoneMixin, TemplateView):
    """ 防火墙端口列表，配置防火墙首页 """
    template_name = 'system/firewalld_port.html'

    def get(self, request, *args, **kwargs):
        if not get_firewalld_state(): return HttpResponseRedirect(reverse('system:firewalld:index'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '配置防火墙许可端口'
        context['breadcrumb'] = [
            {'title': '防火墙', 'href': reverse_lazy('system:firewalld:index'), 'active': False},
            {'title': '防火墙配置', 'href': '', 'active': True},
        ]
        ports = subprocess.run('firewall-cmd --zone=' + context['currentZone'] + ' --list-ports', shell=True,
                                       capture_output=True, encoding="utf-8").stdout.strip('\n')

        context['ports'] = []
        if ports:
            list_ports = ports.split(' ')
            for port in list_ports:
                list_port = port.split('/')
                context['ports'].append({'port': list_port[0], 'protocol': list_port[1]})

        return context


class FirewalldPortAddView(FirewalldGetZoneMixin, FormView):
    """ 添加开放的指定区域端口 """
    template_name = 'system/firewalld_port_add.html'
    form_class = FirewallPortForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '添加许可端口'
        context['breadcrumb'] = [
            {'title': '防火墙', 'href': reverse_lazy('system:firewalld:index'), 'active': False},
            {'title': '端口列表', 'href': reverse_lazy('system:firewalld:port') + '?zone=' + context['currentZone'], 'active': False},
            {'title': '添加端口', 'href': '', 'active': True},
        ]
        return context

    def get_initial(self):
        """ 初始化表单内容."""
        if self.request.method == 'post':
            self.initial['port_type'] = self.request.POST.get('port_type')
            self.initial['zone'] = self.request.POST.get('zone')
            self.initial['port_only'] = self.request.POST.get('port_only')
            self.initial['proto'] = self.request.POST.get('proto')
            self.initial['port_start'] = self.request.POST.get('port_start')
            self.initial['port_end'] = self.request.POST.get('port_end')
        else:
            self.initial['zone'] = self.request.GET.get('zone')
            self.initial['port_type'] = '1'
        return self.initial.copy()

    def form_valid(self, form):
        set_info = {}
        if form.cleaned_data.get('port_type') == '1':
            set_info = subprocess.run(
                'firewall-cmd --add-port={1}/{2} --zone={0} --permanent'
                .format(form.cleaned_data.get('zone'), form.cleaned_data.get('port_only'), form.cleaned_data.get('proto')),
                shell=True, capture_output=True, encoding="utf-8"
            )
        if form.cleaned_data.get('port_type') == '2':
            set_info = subprocess.run(
                'firewall-cmd --zone={0} --add-port={1}-{2}/{3} --permanent'.format(
                    form.cleaned_data.get('zone'), form.cleaned_data.get('port_start'),
                    form.cleaned_data.get('port_end'), form.cleaned_data.get('proto')
                ), shell=True, capture_output=True, encoding="utf-8"
            )
        stderr = set_info.stderr.strip('\n')
        zone = form.cleaned_data.get('zone')
        if not stderr:
            firewalld_reload()
            messages.success(self.request, zone + ' 区域端口添加操作完成！')
            self.success_url = reverse('system:firewalld:port') + '?zone=' + zone
        else:
            messages.warning(self.request, ' 服务器执行错误：' + stderr)
            self.success_url = reverse('system:firewalld:port_add') + '?zone=' + zone

        return super().form_valid(form)


class FirewalldPortDelView(FirewallMixin, RedirectView):
    """ 删除防火墙端口 """
    def post(self, *args, **kwargs):
        zone = self.request.POST.get('zone')
        port = self.request.POST.get('port')
        protocol = self.request.POST.get('protocol')
        set_info = subprocess.run(
            'firewall-cmd --zone={0} --remove-port={1}/{2} --permanent'.format(zone, port, protocol), shell=True,
            capture_output=True, encoding="utf-8"
        )
        messages.success(self.request, zone + ' 区域 ' + port +' 端口 删除完成！')
        firewalld_reload()
        return HttpResponseRedirect(reverse('system:firewalld:port') + '?zone=' + self.request.POST.get('zone'))


class FirewalldServiceView(FirewalldGetZoneMixin, TemplateView):
    """ 防火墙服务列表  """
    template_name = 'system/firewalld_service.html'

    def get(self, request, *args, **kwargs):
        if not get_firewalld_state(): return HttpResponseRedirect(reverse('system:firewalld:index'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '配置防火墙服务许可'
        context['breadcrumb'] = [
            {'title': '防火墙', 'href': reverse_lazy('system:firewalld:index'), 'active': False},
            {'title': '服务列表', 'href': '', 'active': True},
        ]
        system_service = system_services()

        get_services = subprocess.run(
            'firewall-cmd --zone=' + context['currentZone'] + ' --list-services',
            shell=True, capture_output=True, encoding="utf-8").stdout.strip('\n').split(' ')
        context['services'] = []

        while '' in get_services:
            get_services.remove('')
        if len(get_services):
            for service in get_services:
                context['services'].append({
                    'name': service,
                    'short': system_service[service]['short'],
                    'udp': ','.join(system_service[service]['udp']),
                    'tcp': ','.join(system_service[service]['tcp']),
                })

        return context


class FirewalldServiceAddView(FirewalldGetZoneMixin, FormView):
    form_class = FirewallServiceForm
    template_name = 'system/firewalld_service_add.html'

    def get_initial(self):
        """ 初始化表单内容."""
        if self.request.method == 'post':
            self.initial['zone'] = self.request.POST['zone']
            self.initial['service'] = self.request.POST['service']
        else:
            self.initial['zone'] = self.request.GET['zone']
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '添加许可服务'
        context['breadcrumb'] = [
            {'title': '防火墙', 'href': reverse_lazy('system:firewalld:index'), 'active': False},
            {'title': '服务列表', 'href': reverse_lazy('system:firewalld:service') + '?zone=' + context['currentZone'], 'active': False},
            {'title': '添加服务', 'href': '', 'active': True},
        ]
        context['services'] = system_services()
        return context

    def form_valid(self, form):
        run_stderr = subprocess.run(
            'sudo firewall-cmd --permanent --add-service={0}'.format(form.cleaned_data.get('service')),
            shell=True, capture_output=True, encoding="utf-8"
        ).stderr.strip('\n')
        zone = form.cleaned_data.get('zone')
        if run_stderr:
            messages.warning(self.request, '服务器执行错误：' + run_stderr)
            self.success_url = reverse('system:firewalld:service_add') + '?zone=' + zone
        else:
            firewalld_reload()
            messages.success(self.request, zone + ' 区域 添加许可服务 ' + form.cleaned_data.get('service') + '操作完成！')
            self.success_url = reverse('system:firewalld:service') + '?zone=' + zone
        return super().form_valid(form)


class FirewalldServiceDelView(RedirectView):
    query_string = True
    url = reverse_lazy('system:firewalld:service')

    def post(self, request, *args, **kwargs):
        zone = self.request.POST.get('zone')
        service = self.request.POST.get('service')
        print('firewall-cmd --permanent --remove-service {0}'.format(service))
        run_stderr = subprocess.run(
            'firewall-cmd --permanent --remove-service {0}'.format(service), shell=True, capture_output=True, encoding="utf-8"
        ).stderr.strip('\n')
        if run_stderr:
            messages.warning(self.request, '服务器执行错误：' + run_stderr)
        else:
            firewalld_reload()
            messages.success(self.request, zone + ' 区域删除 ' + service + ' 服务操作完成！')

        return self.get(request, *args, **kwargs)