import subprocess

from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, RedirectView
from django.contrib import messages
from django.http import JsonResponse

from .views_system import SystemMixin
from .forms import ConnForm


def check_con_name(request):
    """ 检测是否有重复连接名称 """
    con_name = request.GET.get('fieldValue')
    con_name_list = subprocess.run(
        'nmcli -g name con show', shell=True, capture_output=True, encoding='utf-8').stdout.strip('\n').split('\n')
    if con_name in con_name_list:
        return JsonResponse(['id_name', False], safe=False)
    else:
        return JsonResponse(['id_name', True], safe=False)


def get_cons():
    get_con_name_list = subprocess.run(
        'nmcli -g name con show', shell=True, capture_output=True, encoding='utf-8').stdout.strip('\n').split('\n')
    get_con_type_list = subprocess.run(
        'nmcli -f uuid,type con show', shell=True, capture_output=True, encoding='utf-8').stdout.strip('\n').split('\n')
    del get_con_type_list[0]
    get_con_list = subprocess.run(
        'nmcli -g uuid,type,autoconnect,device,state,filename,active con show',
        shell=True, capture_output=True, encoding='utf-8'
    ).stdout.strip('\n').split('\n')

    base_list = {}
    i = 0
    for con in get_con_list:
        con_base = con.split(":")
        base_list[con_base[0]] = {
                'name': get_con_name_list[i].replace('\\', ''), 'uuid': con_base[0], 'autoconnect': con_base[2],
                'device': con_base[3] if con_base[3] else '', 'state': con_base[4] if con_base[4] else '',
                'filename': con_base[5], 'active': con_base[6]
            }
        for con_type_value in get_con_type_list:
            con_type_list = con_type_value.strip().split('  ')
            con_uuid = con_type_list[0].strip()
            con_type = con_type_list[1].strip()
            if con_base[0] == con_uuid:
                base_list[con_base[0]]['type'] = con_type
        i = i + 1

    return_list = {}
    for uuid, info in base_list.items():
        con_show = subprocess.run(
            'nmcli con show "' + uuid + '"', shell=True, capture_output=True, encoding='utf-8'
        ).stdout.strip().split('\n')

        return_list[uuid] = info
        return_list[uuid]['ipv4addr'] = ''
        return_list[uuid]['ipv4dnsm'] = ''
        return_list[uuid]['ipv4address'] = []
        return_list[uuid]['ipv6address'] = []
        return_list[uuid]['macaddress'] = ''
        return_list[uuid]['ipv4dns'] = []

        for con_str in con_show:
            str_list = con_str.split(': ')
            if len(str_list) == 2:
                name_str = str_list[0] + ':'
                if 'connection.id:' in name_str:
                    return_list[uuid]['id'] = str_list[1].replace(' ', '')
                if 'GENERAL.DEVICE:' in name_str:
                    return_list[uuid]['device'] = str_list[1].replace(' ', '')
                if 'ipv4.method:' in name_str:
                    return_list[uuid]['ipv4method'] = str_list[1].replace(' ', '')
                    return_list[uuid]['ipv4method_cn'] = '-'
                    if return_list[uuid]['ipv4method'] == 'auto':
                        return_list[uuid]['ipv4method_cn'] = '自动(DHCP)'
                    if return_list[uuid]['ipv4method'] == 'manual':
                        return_list[uuid]['ipv4method_cn'] = '手动'
                if 'ipv4.addresses:' in name_str:
                    return_list[uuid]['ipv4'] = str_list[1].replace(' ', '').split(', ')
                if 'ipv6.method:' in name_str:
                    return_list[uuid]['ipv6method'] = str_list[1].replace(' ', '')
                    return_list[uuid]['ipv6method_cn'] = '-'
                    if return_list[uuid]['ipv6method'] == 'auto':
                        return_list[uuid]['ipv6method_cn'] = '自动(DHCP)'
                    if return_list[uuid]['ipv6method'] == 'manual':
                        return_list[uuid]['ipv6method_cn'] = '手动'
                if 'ipv4.addresses:' in name_str:
                    return_list[uuid]['ipv4addr'] = str_list[1].strip()
                if 'ipv4.dns:' in name_str:
                    return_list[uuid]['ipv4dnsm'] = str_list[1].strip()
                if 'IP4.ADDRESS[' in name_str:
                    return_list[uuid]['ipv4address'].append(str_list[1].strip())
                if 'IP6.ADDRESS[' in name_str:
                    return_list[uuid]['ipv6address'].append(str_list[1].strip())
                if 'connection.type:' in name_str:
                    return_list[uuid]['connectiontype'] = str_list[1].strip()
                if '.mac-address:' in name_str:
                    return_list[uuid]['macaddress'] = str_list[1].strip()
                if 'IP4.GATEWAY:' in name_str:
                    return_list[uuid]['ipv4geway'] = str_list[1].strip()
                if 'IP4.DNS[' in name_str:
                    return_list[uuid]['ipv4dns'].append(str_list[1].strip())

    return return_list


def get_devices():
    con_name_list = subprocess.run('nmcli -g GENERAL.DEVICE dev show', shell=True, capture_output=True, encoding="utf-8"
                                   ).stdout.strip('\n').split('\n\n')
    return_list = {}
    for con_name in con_name_list:
        return_list[con_name] = {}
        con_show_list = subprocess.run(
            'nmcli -f GENERAL,CAPABILITIES,IP4,DHCP4,IP6,DHCP6 dev show "' + con_name + '"',
            shell=True, capture_output=True, encoding="utf-8").stdout.strip('\n').split('\n\n')
        for con_set_str in con_show_list:
            con_set_list = con_set_str.split('\n')
            return_list[con_name]['ipv4address'] = []
            return_list[con_name]['ipv6address'] = []
            for con_set in con_set_list:
                con = con_set.split(': ')
                if 'GENERAL.TYPE:' in con_set:
                    return_list[con_name]['type'] = con[1].strip()
                if 'GENERAL.NM-TYPE:' in con_set:
                    return_list[con_name]['nmtype'] = con[1].strip()
                if 'GENERAL.VENDOR:' in con_set:
                    return_list[con_name]['venddr'] = con[1].strip()
                if 'GENERAL.PRODUCT:' in con_set:
                    return_list[con_name]['product'] = con[1].strip()
                if 'GENERAL.HWADDR:' in con_set:
                    return_list[con_name]['hwaddr'] = con[1].strip()
                if 'GENERAL.NM-TYPE:' in con_set:
                    return_list[con_name]['nmtype'] = con[1].strip()
                if 'GENERAL.MTU:' in con_set:
                    return_list[con_name]['mtu'] = con[1].strip()
                if 'GENERAL.STATE:' in con_set:
                    return_list[con_name]['sate'] = con[1].strip()
                if 'GENERAL.AUTOCONNECT:' in con_set:
                    return_list[con_name]['autoconnect'] = con[1].strip()
                if 'GENERAL.CONNECTION:' in con_set:
                    return_list[con_name]['connection'] = con[1].strip()
                if 'GENERAL.CON-UUID:' in con_set:
                    return_list[con_name]['conuuid'] = con[1].strip()
                if 'CAPABILITIES.SPEED:' in con_set:
                    return_list[con_name]['capspeed'] = con[1].strip()
                if 'CAPABILITIES.IS-SOFTWARE:' in con_set:
                    return_list[con_name]['capissoftware'] = con[1].strip()
                if 'IP6.ADDRESS[' in con_set:
                    return_list[con_name]['ipv6address'].append(con[1].strip())
                if 'IP4.ADDRESS[' in con_set:
                    return_list[con_name]['ipv4address'].append(con[1].strip())

    # con_list = subprocess.run('nmcli dev show', shell=True, capture_output=True, encoding="utf-8") \
    #     .stdout.strip('\n').split('\n\n')
    # list = {}
    # for con in con_list:
    #     con_list = con.split('\n')
    #     for con_item in con_list:
    #         con_item_list = con_item.split(':  ')
    #         con_item_list = [i for i in con_item_list if i != '']
    #         if 'GENERAL.DEVICE' in con_item_list[0]:
    #             device = con_item_list[1].strip()
    #             list[device] = {}
    #             list[device]['ipv4address'] = []
    #             list[device]['ipv4route'] = []
    #             list[device]['ipv4dns'] = []
    #             list[device]['ipv4domain'] = []
    #             list[device]['ipv6address'] = []
    #             list[device]['ipv6route'] = []
    #             list[device]['ipv6dns'] = []
    #             list[device]['ipv6domain'] = []
    #         if 'GENERAL.TYPE' in con_item_list[0]:
    #             list[device]['devicetype'] = con_item_list[1].strip()
    #         if 'GENERAL.HWADDR' in con_item_list[0]:
    #             list[device]['hwaddr'] = con_item_list[1].strip()
    #         if 'GENERAL.MTU' in con_item_list[0]:
    #             list[device]['mtu'] = con_item_list[1].strip()
    #         if 'GENERAL.STATE' in con_item_list[0]:
    #             list[device]['devicestate'] = con_item_list[1].strip()
    #         if 'GENERAL.CONNECTION' in con_item_list[0]:
    #             list[device]['connection'] = con_item_list[1].strip()
    #         if 'GENERAL.CON-PATH' in con_item_list[0]:
    #             list[device]['conpath'] = con_item_list[1].strip()
    #         if 'WIRED-PROPERTIES.CARRIER' in con_item_list[0]:
    #             list[device]['wiredpropertiescarrier'] = con_item_list[1].strip()
    #         if 'GENERAL.MTU' in con_item_list[0]:
    #             list[device]['mtu'] = con_item_list[1].strip()
    #         if 'GENERAL.MTU' in con_item_list[0]:
    #             list[device]['mtu'] = con_item_list[1].strip()
    #         if 'IP4.ADDRESS' in con_item_list[0]:
    #             list[device]['ipv4address'].append(con_item_list[1].strip())
    #         if 'IP4.GATEWAY' in con_item_list[0]:
    #             list[device]['ipv4getway'] = con_item_list[1].strip()
    #         if 'IP4.ROUTE' in con_item_list[0]:
    #             list[device]['ipv4route'].append(con_item_list[1].strip())
    #         if 'IP4.DOMAIN' in con_item_list[0]:
    #             list[device]['ipv4domain'].append(con_item_list[1].strip())
    #         if 'IP6.ADDRESS' in con_item_list[0]:
    #             list[device]['ipv6address'].append(con_item_list[1].strip())
    #         if 'IP6.GATEWAY' in con_item_list[0]:
    #             list[device]['ipv6getway'] = con_item_list[1].strip()
    #         if 'IP6.ROUTE' in con_item_list[0]:
    #             list[device]['ipv6route'].append(con_item_list[1].strip())
    #         if 'IP6.DOMAIN' in con_item_list[0]:
    #             list[device]['ipv6domain'].append(con_item_list[1].strip())
    return return_list


class NetworkContextMixin(SystemMixin):
    """ 网络配置基础参数 """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'network'
        return context


class DeviceListView(NetworkContextMixin, TemplateView):
    template_name = 'system/network_device.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '网络'
        context['devices'] = get_devices()
        return context


class DeviceDetailView(NetworkContextMixin, TemplateView):
    template_name = 'system/network_device_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devicename'] = self.kwargs.get('device')
        context['page_title'] = '网络接口 - ' + context['devicename']
        context['breadcrumb'] = [
            {'title': '网络', 'href': reverse_lazy('system:network:device'), 'active': False},
            {'title': '网络接口 - ' + context['devicename'], 'href': '', 'active': True},
        ]
        context['deviceinfo'] = get_devices()[context['devicename']]
        context['connlist'] = get_cons()
        return context


class ConnModifyView(NetworkContextMixin, FormView):
    form_class = ConnForm
    template_name = 'system/network_conn_add.html'

    def get_success_url(self):
        self.success_url = reverse('system:network:device_detail', kwargs={'device': self.kwargs.get('device')})
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dev_name = self.kwargs.get('device')
        context['page_title'] = dev_name + ' - 新配置'
        context['device_name'] = dev_name
        context['device'] = get_devices()[dev_name]
        context['breadcrumb'] = [
            {'title': '网络', 'href': reverse_lazy('system:network:device'), 'active': False},
            {
                'title': '网络接口 - ' + dev_name,
                'href': reverse_lazy('system:network:device_detail', kwargs={'device': dev_name}),
                'active': False
            },
            {'title': dev_name + ' 新配置 ', 'href': '', 'active': True},
        ]
        context['conn'] = get_cons()
        return context

    def get_initial(self):
        self.initial['autoconnect'] = 'True'
        self.initial['ipv4method'] = 'auto'
        return self.initial.copy()

    def form_valid(self, form):
        device = self.kwargs.get('device')
        mac = get_devices()[device]['hwaddr']
        name = form.cleaned_data.get('name')
        ipv4method = form.cleaned_data.get('ipv4method')
        ip4 = form.cleaned_data.get('ip4')
        gw4 = form.cleaned_data.get('gw4')
        ip4dns = form.cleaned_data.get('ip4dns')

        run_str = 'nmcli conn add con-name "' + name + '" type "ethernet" ifname "' + device + \
                  '" ethernet.mac-address "' + mac + '" ipv4.method "' + ipv4method + '"'

        mtu = form.cleaned_data.get('mtu')
        autoconnect = form.cleaned_data.get('autoconnect')
        if autoconnect == 'False':
            run_str += ' autoconnect no'
        if mtu:
            run_str += ' mtu ' + mtu
        if ip4:
            run_str += ' ip4 "' + ip4 + '"'
        if gw4:
            run_str += ' gw4 "' + gw4 + '"'
        if ip4dns:
            run_str += ' ipv4.dns "' + ip4dns + '"'
        run = subprocess.run(run_str, shell=True, capture_output=True, encoding="utf-8")
        return super().form_valid(form)


class ConnActiveView(NetworkContextMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('system:network:device_detail', kwargs={'device': kwargs.get('device')})

    def get(self, request, *args, **kwargs):
        action = self.kwargs.get('action')
        uuid = self.kwargs.get('uuid')
        run = subprocess.run(
            'nmcli conn ' + action + ' "' + uuid + '"', shell=True, capture_output=True, encoding="utf-8")

        if run.stderr:
            messages.warning(self.request, ' 服务器执行结果：' + run.stderr)
        else:
            messages.success(self.request, ' 网络连接操作执行成功！')

        return super().get(request, *args, **kwargs)


# class ConnsListView(NetworkContextMixin, TemplateView):
#     template_name = 'system/network_conn.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = '网络连接'
#         # conn_list = get_con()
#         # print(conn_list)
#         # af_map = {
#         #     socket.AF_INET: 'ipv4',
#         #     socket.AF_INET6: 'ipv6',
#         #     psutil.AF_LINK: 'mac',
#         # }
#         # stats = psutil.net_if_stats()
#         # list = []
#         # net_nic = subprocess.run(
#         #     'ls /sys/class/net/ | grep -v "$(ls /sys/devices/virtual/net/)"',
#         #     shell=True, capture_output=True, encoding="utf-8"
#         # ).stdout.strip('\n').split('\n')
#
#         # v_nic = subprocess.run('ls /sys/devices/virtual/net/',shell=True, capture_output=True, encoding="utf-8")\
#         #     .stdout.strip('\n').split('\n')
#         # for nic, addrs in psutil.net_if_addrs().items():
#         #     interface = {'device': nic, 'type': '-'}
#         #     if nic in v_nic: interface['type'] = '虚拟'
#         #     if nic in net_nic: interface['type'] = '物理'
#         #     if nic in stats:
#         #         st = stats[nic]
#         #         interface['up'] = "启用" if st.isup else "禁用"
#         #     for addr in addrs:
#         #         ipv_type = af_map.get(addr.family, addr.family)
#         #         interface[ipv_type + 'address'] = addr.address
#         #         if addr.netmask:
#         #             interface[ipv_type + 'netmask'] = addr.netmask
#         #
#         #     list.append(interface)
#
#         # devices = get_devices()
#         # conns = get_cons()
#         # list = {}
#         # # 合并连接和设备的信息
#         # for k, v in conns.items():
#         #     print(v)
#         #     if 'device' in v and v['device'] != '--':
#         #         v.update(devices[v['device']])
#         #     list[k] = v
#         context['list'] = get_cons()
#         return context
#
#
# class ConnDetailView(NetworkContextMixin, FormView):
#     form_class = ConnRenameForm
#     template_name = 'system/network_conn_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = '配置网络连接'
#         context['breadcrumb'] = [
#             {'title': '网络连接', 'href': reverse_lazy('system:network:conn'), 'active': False},
#             {'title': '配置网络连接', 'href': '', 'active': True},
#         ]
#         context['uuid'] = self.kwargs.get('uuid')
#         context['con'] = get_cons()[self.kwargs.get('uuid')]
#         context['action'] = ''
#         if 'action' in self.request.GET:
#             context['action'] = self.request.GET.get('action')
#         return context
#
#     def form_valid(self, form):
#         action = self.request.GET.get('action')
#         uuid = self.kwargs.get('uuid')
#         if action == 'rename':
#             newname = form.cleaned_data.get('newname')
#             run = subprocess.run(
#                 'nmcli con modify "' + uuid + '" connection.id "' + newname + '"',
#                 shell=True, capture_output=True, encoding="utf-8"
#             )
#             if run.stderr:
#                 messages.warning(self.request, '服务器执行错误：' + run.stderr)
#         self.success_url = reverse('system:network:conn_detail', kwargs={'uuid': uuid})
#
#         return super().form_valid(form)
#
#
# class ConnActionView(NetworkContextMixin, RedirectView):
#
#     def get(self, request, *args, **kwargs):
#         action = self.kwargs.get('action')
#         uuid = self.kwargs.get('uuid')
#         flag = True
#         self.url = reverse('system:network:conn_detail', kwargs={"uuid": uuid})
#         run_check = subprocess.run(
#             'nmcli -g name,state con show', shell=True, capture_output=True, encoding='utf-8').stdout.strip().split('\n')
#         print(run_check)
#
#         if action == 'delete':
#             if len(run_check) == 1:
#                 messages.warning(self.request, '至少要保留一个可用网络连接!')
#                 flag = False
#             else:
#                 self.url = reverse('system:network:conn')
#         if action == 'down' and len(run_check) == 1 and ':activated' in run_check[0]:
#             messages.warning(self.request, '至少要保留一个可用网络连接!')
#             flag = False
#
#         if flag:
#             # if action == 'up' or action == 'down' or action == 'delete':
#             run = subprocess.run(
#                 'nmcli conn ' + action + ' "' + uuid + '"', shell=True, capture_output=True, encoding="utf-8")
#             if run.stderr:
#                 messages.warning(self.request, '服务器执行错误：' + run.stderr)
#         return super().get(request, *args, **kwargs)
#
#
# class ConnAddView(NetworkContextMixin, FormView):
#     template_name = 'system/network_conn_form.html'
#     form_class = ConnForm
#
# class DevicesView(NetworkContextMixin, TemplateView):
#     template_name = 'system/network_devices.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = '网络设备'
#         context['list'] = get_devices()
#         return context

