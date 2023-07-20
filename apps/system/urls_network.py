from django.urls import path
from django.contrib.auth.decorators import login_required

from apps.system import view_network

app_name = 'network'

urlpatterns = [
    path('device/list/', login_required(view_network.DeviceListView.as_view()), name='device'),
    path('device/detail/<str:device>', login_required(view_network.DeviceDetailView.as_view()), name='device_detail'),
    path('conn/<str:action>/<str:uuid>/<str:device>', login_required(view_network.ConnActiveView.as_view()), name='conn_action'),
    path('conn/add/<str:device>', login_required(view_network.ConnModifyView.as_view()), name='conn_add'),
    path('conn/check/', login_required(view_network.check_con_name), name='conn_check_name'),
]