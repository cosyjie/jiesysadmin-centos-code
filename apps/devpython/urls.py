from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'devpython'

urlpatterns = [
    path('index/', login_required(views.PythonView.as_view()), name='index'),
    path('delete/<str:version>/', login_required(views.PythonDelView.as_view()), name='del'),
    path('install/', login_required(views.PythonInstallView.as_view()), name='install'),
    path('install/download/', login_required(views.python_download), name='install_download'),
    path('install/run/', login_required(views.python_install_run),name='install_run'),
    path('test/', login_required(views.import_iter), name='test'),
    # path('installing/<str:setup>/<str:version>/<str:website>/', views.PythonInstallingView.as_view(), name='setup'),
]