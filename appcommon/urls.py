from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'site_home'

urlpatterns = [
    path('index/', login_required(views.SiteHomeView.as_view()), name='index'),
    path('shutdown/<str:action>', login_required(views.Shutdown.as_view()), name='shutdown'),
    path('hostname/', login_required(views.HostnameView.as_view()), name='hostname'),

]