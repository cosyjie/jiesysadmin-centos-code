from django.urls import path
from django.contrib.auth.decorators import login_required

from apps.system import view_process

app_name = 'process'

urlpatterns = [
    path('list/<str:listtype>', login_required(view_process.ProcessListView.as_view()), name='list'),
    path('detail/<str:listtype>/<int:pid>', login_required(view_process.DetailView.as_view()), name='detail'),
    path('action/<str:listtype>/<str:action>/<int:pid>', login_required(view_process.ActionView.as_view()), name='action')
]