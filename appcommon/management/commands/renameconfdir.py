import os, shutil, sys, datetime
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dirname',
            help='Please enter new django settings folder name。',
        )
    
    def handle(self, **options):

        if options['dirname']:
            dir_name = options['dirname']
        else:
            dir_name = 'conf'
        if dir_name:
            #获取当前文件路径参数
            base_dir = settings.BASE_DIR
            settings_path_list = os.environ['DJANGO_SETTINGS_MODULE'].split('.')
            settings_dir_list = settings_path_list[:-2]
            settings_dirname = settings_path_list[-2]
            settings_file_name = settings_path_list[-1]
            # 配置文件文件夹路径
            settings_dir = base_dir
            for value in settings_dir_list:
                settings_dir += os.path.join(settings_dir, value)

            try:
                # 修改配置文件夹名
                os.rename(os.path.join(base_dir, settings_dirname), os.path.join(base_dir, dir_name))

                # 读取并重写配置目录下的 settings 文件内容
                file = os.path.join(base_dir, dir_name, settings_file_name + '.py')
                get_content = open(file, 'r', encoding='utf-8').read()
                content = get_content.replace(settings_dirname + '.wsgi.application', dir_name + '.wsgi.application')
                content = content.replace(settings_dirname + '.urls', dir_name + '.urls')
                open(file, 'w', encoding='utf-8').write(content)

                # 读取并重写配置目录下的 asgi.py 文件内容
                file = os.path.join(base_dir, dir_name, 'asgi.py')
                get_content = open(file, 'r', encoding='utf-8').read()
                content = get_content.replace(settings_dirname + '.' + settings_file_name, dir_name + '.' + settings_file_name)
                open(file, 'w', encoding='utf-8').write(content)

                # 读取并重写 wsgi.py 文件内容
                file = os.path.join(base_dir, dir_name, 'wsgi.py')
                get_content = open(file, 'r', encoding='utf-8').read()
                content = get_content.replace(settings_dirname + '.' + settings_file_name, dir_name + '.' + settings_file_name)
                open(file, 'w', encoding='utf-8').write(content)

                # 读取并重写项目根目录的 manage.py
                get_content = open(os.path.join(base_dir, 'manage.py'), 'r', encoding='utf-8').read()
                content = get_content.replace(settings_dirname + '.' + settings_file_name, dir_name + '.' + settings_file_name)
                open(os.path.join(base_dir, 'manage.py'), 'w', encoding='utf-8').write(content)

            except OSError as e:
                raise CommandError(e)
                

        

        