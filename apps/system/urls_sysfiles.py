from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import view_sysfiles

app_name = 'sysfiles'

urlpatterns = [
    path('list/', login_required(view_sysfiles.ListView.as_view()), name='list'),
    path('edit/', login_required(view_sysfiles.FileEditView.as_view()), name='edit'),
    path('del/<str:filetype>/', login_required(view_sysfiles.FileDelView.as_view()), name='del'),
    path('dir/<str:action>/', login_required(view_sysfiles.FileDirNameView.as_view()), name='dir'),
    path('upload/', login_required(view_sysfiles.FileUploadView.as_view()), name='upload'),
    path('download/', login_required(view_sysfiles.FileDownloadView.as_view()), name='download'),
]