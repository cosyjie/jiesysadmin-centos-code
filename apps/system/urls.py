from django.urls import path, include
from . import view_xterm

app_name = 'system'

urlpatterns = [
    path('firewalld/', include('apps.system.urls_firewalld', namespace='firewalld')),
    path('network/', include('apps.system.urls_network', namespace='network')),
    path('process/', include('apps.system.urls_process', namespace='process')),
    # path('terminal/', view_xterm.index, name='terminal'),
    path('sysfiles/', include('apps.system.urls_sysfiles', namespace='sysfiles')),
]