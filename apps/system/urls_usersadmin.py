from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import view_usersadmin

app_name = 'usersadmin'

urlpatterns = [
    path('list/', login_required(view_usersadmin.UsersListView.as_view()), name='list'),
    path('detail/<str:username>/', login_required(view_usersadmin.UserDetailView.as_view()), name='detail'),
    path('create/', login_required(view_usersadmin.UsersAddView.as_view()), name='add'),
    path('password/<str:user>/', login_required(view_usersadmin.UserPwdView.as_view()), name='pwd'),
    path('current/', login_required(view_usersadmin.UserWhoListView.as_view()), name='who_list'),
    path('kill/', login_required(view_usersadmin.UserKillView.as_view()), name='who_kill'),
    path('delete/<str:user>/', login_required(view_usersadmin.UserDelView.as_view()), name='del'),
]

