from django.urls import reverse

menu = {
    'system': {
        'title': '系统管理',
        'href': '',
        'ico': 'fas  fa-laptop',
        'child': [
            {'name': 'firewalld', 'title': '防火墙', 'href': reverse('system:firewalld:index')},
            {'name': 'network', 'title': '网络', 'href': reverse('system:network:device')},
            {'name': 'process', 'title': '进程管理', 'href': reverse('system:process:list', kwargs={'listtype': 'all'})},
            # {'name': 'terminal', 'title': '终端', 'href': reverse('system:terminal')},
            {'name': 'sysfiles', 'title': '文件管理', 'href': reverse('system:sysfiles:list')},
            {'name': 'usersadmin', 'title': '用户', 'href': reverse('system:usersadmin:list')},
            {'name': 'timezone', 'title': '时区和时间', 'href': reverse('system:timezone:index')},

        ]
    }
}
