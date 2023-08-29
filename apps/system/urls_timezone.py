from django.urls import path
from django.contrib.auth.decorators import login_required


from . import view_timezone

app_name = 'timezone'

urlpatterns = [
    path('index/', login_required(view_timezone.TimezoneView.as_view()), name='index'),

]