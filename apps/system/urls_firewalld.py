from django.urls import path
from django.contrib.auth.decorators import login_required

from apps.system import view_firewalld

app_name = 'firewalld'

urlpatterns = [
    path('index/', login_required(view_firewalld.FirewalldView.as_view()), name='index'),
    path('action/', login_required(view_firewalld.FirewalldActionView.as_view()), name='action'),
    path('reload/', login_required(view_firewalld.FirewalldReloadView.as_view()), name='reload'),
    path('port/list/', login_required(view_firewalld.FirewalldPortView.as_view()), name='port'),
    path('port/add/', login_required(view_firewalld.FirewalldPortAddView.as_view()), name='port_add'),
    path('port/del/', login_required(view_firewalld.FirewalldPortDelView.as_view()), name='port_del'),
    path('service/list/', login_required(view_firewalld.FirewalldServiceView.as_view()), name='service'),
    path('service/add/', login_required(view_firewalld.FirewalldServiceAddView.as_view()), name='service_add'),
    path('service/del/', login_required(view_firewalld.FirewalldServiceDelView.as_view()), name='service_del'),

]