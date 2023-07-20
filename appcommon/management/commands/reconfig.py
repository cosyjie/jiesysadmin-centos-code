import os, shutil, sys, datetime
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    def handle(self, **options):
        #获取当前文件路径
        current_dir = Path(__file__).resolve().parent.parent.parent
        secret_key = settings.SECRET_KEY
        root_urlconf = settings.ROOT_URLCONF
        wsgi_application = settings.WSGI_APPLICATION

        #获取原 settings 文件路径
        old_settings_file_list = os.environ['DJANGO_SETTINGS_MODULE'].split('.')
        settings_dir_list = old_settings_file_list[:-1]
        settings_dir = settings.BASE_DIR
        # 配置文件目录
        for value in settings_dir_list:
            settings_dir = os.path.join(settings_dir, value)

        # 替换 URLS 文件
        urls_path = os.path.join(settings_dir, 'urls.py')

        content = '''
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from cosyframesingle.views import siteviews

urlpatterns = [
    path('', siteviews.CosyLoginView.as_view(), name='site_login'),
    path('login/', siteviews.CosyLoginView.as_view(), name='site_login'),
    path('logout/', siteviews.CosyLayoutView.as_view(), name='site_logout'),
    path('home/', login_required(siteviews.SiteHomeView.as_view()), name='site_home'),
    path('password_reset/reset', siteviews.ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset/reset/done/', siteviews.ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', siteviews.ResetPasswordConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset/complete/', siteviews.ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
    path('my/', include('cosyframesingle.urls.urls_frame_profile', namespace='site_profile')),
    path('system/', include('cosyframesingle.urls.urls_frame_system', namespace='frame_system')),
]
'''        
        open(urls_path, 'w', encoding='utf-8').write(content)
        
        # 原配置文件路径
        settings_file = settings.BASE_DIR
        for value in old_settings_file_list:
            settings_file = os.path.join(settings_file, value)
        settings_file = settings_file + '.py'
        # 原配置文件备份
        bak_dir = os.path.join(settings_dir, 'bak')
        if not os.path.exists(bak_dir):
            os.mkdir(bak_dir)
        shutil.copyfile(
            settings_file, os.path.join(bak_dir, 'settings.py' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        )

        # 替换 config 文件
        frame_config = os.path.join(current_dir, 'config.py')
        content = open(frame_config, 'r', encoding='utf-8').read().replace('{{0}}', secret_key).replace('{{1}}', wsgi_application).replace('{{2}}', root_urlconf)

        # 替换系统 settings 文件
        open(settings_file, 'w', encoding='utf-8').write(content)

        
