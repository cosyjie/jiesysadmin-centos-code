from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from appcommon import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.CosyLoginView.as_view()),
    path('login/', views.CosyLoginView.as_view(), name='site_login'),
    path('logout/', login_required(views.CosyLayoutView.as_view()), name='site_logout'),
    path('home/', include('appcommon.urls', namespace='site_home')),
    path('system/', include('apps.system.urls', namespace='system')),
    path('devpython/', include('apps.devpython.urls', namespace='devpython')),

]

urlpatterns += staticfiles_urlpatterns()
