import stat
import pwd
import shutil
import os
import subprocess

from datetime import datetime
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .views_system import SystemMixin

from .forms import FileEditForm, FileDirForm, FileUploadForm, FileDownloadForm


class SysfilesMixin(SystemMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'sysfiles'
        return context


class ListView(SysfilesMixin, TemplateView):
    template_name = 'system/files_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '文件列表'
        context['path'] = '/'
        context['dirlist'] = {}
        context['parentdir'] = ''
        dirs = {}
        files = {}
        if 'path' in self.request.GET:
            context['path'] = self.request.GET.get('path')
            if context['path'][-1] != '/':
                context['path'] += '/'
        try:
            for file_name in os.listdir(context['path']):
                path = os.path.join(context['path'], file_name)
                file_stat = os.stat(path)
                st_mode = file_stat.st_mode
                st_uid = file_stat.st_uid
                st_size = file_stat.st_size
                st_mtime = file_stat.st_mtime
                type_en = ''
                type_cn = ''

                if stat.S_ISDIR(st_mode):
                    type_en = 'd'
                    type_cn = '目录'
                    if os.path.islink(path):
                        type_en = 'ld'
                        type_cn = '链接目录'
                if stat.S_ISREG(st_mode):
                    type_en = '-'
                    type_cn = '文件'
                    if os.path.islink(path):
                        type_en = 'l'
                        type_cn = '链接文件'
                    if stat.S_ISSOCK(st_mode):
                        type_en = 's'
                        type_cn = '套接字文件'
                    if stat.S_ISBLK(st_mode):
                        type_en = 'b'
                        type_cn = '块设备'
                    if stat.S_ISCHR(st_mode):
                        type_en = 'c'
                        type_cn = '字符设置文件'
                    if stat.S_ISFIFO(st_mode):
                        type_en = 'p'
                        type_cn = '管理文件'
                try:
                    getpw = pwd.getpwuid(st_uid)
                    pw_name = getpw.pw_name
                    pw_gecos = getpw.pw_gecos
                except KeyError:
                    pw_name = '-'
                    pw_gecos = '-'
                tmp = {
                        'type_en': type_en,
                        'type_cn': type_cn,
                        'auth': stat.filemode(st_mode) + '(' + oct(st_mode & 0o777).replace('0o', '') + ')',
                        'owner': pw_name,
                        'group': pw_gecos,
                        'st_size': st_size,
                        'at_time': datetime.fromtimestamp(st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                 }
                if type_en == 'd' or type_en == 'ld':
                    dirs[file_name] = tmp
                else:
                    files[file_name] = tmp

            if dirs:
                sorted_keys = sorted(dirs.keys())
                dirs = {k: dirs[k] for k in sorted_keys}
            if files:
                sorted_keys = sorted(files.keys())
                files = {k: files[k] for k in sorted_keys}
            context['dirlist'] = dict(dirs, **files)
            context['parentdir'] = os.path.abspath(os.path.join(context['path'], '..'))
        except FileNotFoundError:
            messages.error(self.request, '无法找到路径：' + context['path'])
        except PermissionError:
            messages.error(self.request, '无权限访问路径：' + context['path'])
        return context


class FileEditView(SysfilesMixin, FormView):
    template_name = 'system/files_edit.html'
    form_class = FileEditForm

    def get_success_url(self):
        self.success_url = reverse('system:sysfiles:list') + '?path=' + self.request.GET.get('path')
        return super().get_success_url()

    def get_initial(self):
        self.initial['path'] = self.request.GET.get('path')
        self.initial['filename'] = self.request.GET.get('filename')
        self.initial['filecontent'] = ''

        if self.initial['filename']:
            filepath = os.path.join(self.initial['path'], self.initial['filename'])
            try:
                with open(filepath, 'r') as f:
                    self.initial['filecontent'] = f.read()
            except:
                self.initial['filecontent'] = ''
            finally:
                f.close()
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '编辑文件内容'
        context['filename'] = self.request.GET.get('filename')
        context['path'] = self.request.GET.get('path')
        context['breadcrumb'] = [{
            'title': '文件列表',
            'href': reverse('system:sysfiles:list') + '?path=' + context['path'],
            'active': False},
            {'title': '编辑文件信息', 'href': '', 'active': True},
        ]
        context['check'] = True
        if context['filename']:
            file_path = os.path.join(context['path'], context['filename'])
            try:
                with open(file_path, encoding='utf-8') as f: pass
            except:
                context['check'] = False

        return context

    def form_valid(self, form):
        path = form.cleaned_data.get('path')
        filename = form.cleaned_data.get('filename')
        filecontent = form.cleaned_data.get('filecontent').replace('\r\n', '\n').replace('\r', '\n')
        filepath = os.path.join(path, filename)
        file = open(filepath, 'w')
        file.write(filecontent)
        file.close()
        return super().form_valid(form)


class FileDelView(SysfilesMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('system:sysfiles:list') + '?path=' + self.request.GET.get("path")

    def get(self, request, *args, **kwargs):
        filetype = kwargs['filetype']
        filetype_cn = ''
        path = request.GET.get('path')
        filename = request.GET.get('filename')
        filepath = os.path.join(path, filename)
        try:
            if filetype == 'file':
                os.remove(filepath)
                filetype_cn = '文件'
            if filetype == 'dir':
                shutil.rmtree(filepath)
                filetype_cn = '目录'
            messages.success(request, "删除{} {} 成功".format(filetype_cn, filename))
        except OSError as e:
            messages.warning(request, "删除{} {} 出错: {}".format(filetype_cn, filename, e))

        return super().get(request, *args, **kwargs)


class FileDirNameView(SysfilesMixin, FormView):
    form_class = FileDirForm
    template_name = 'system/files_dir_form.html'

    def get_initial(self):
        self.initial = super().get_initial()
        self.initial['path'] = self.request.GET.get('path')
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '创建目录'
        context['path'] = self.request.GET.get('path')
        context['breadcrumb'] = [{
            'title': '文件列表',
            'href': reverse('system:sysfiles:list') + '?path=' + context['path'],
            'active': False},
            {'title': '创建目录', 'href': '', 'active': True},
        ]
        return context

    def form_valid(self, form):
        path = form.cleaned_data.get('path')
        name = form.cleaned_data.get('name')
        try:
            os.mkdir(os.path.join(path, name))
            messages.success(self.request, "创建 {} 成功".format(name))
            self.success_url = reverse('system:sysfiles:list') + '?path=' + path
        except OSError as e:
            self.success_url = reverse('system:sysfiles:dir', kwargs={'action': 'create'}) + '?path=' + path
            messages.warning(self.request, "创建 {} 出错: {}".format(name, e))

        return super().form_valid(form)


class FileUploadView(SysfilesMixin, FormView):
    form_class = FileUploadForm
    template_name = 'system/files_upload.html'

    def get_initial(self):
        self.initial = super().get_initial()
        self.initial['path'] = self.request.GET.get('path')
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '上传文件'
        context['path'] = self.request.GET.get('path')
        context['breadcrumb'] = [{
            'title': '文件列表',
            'href': reverse('system:sysfiles:list') + '?path=' + context['path'],
            'active': False},
            {'title': '上传文件', 'href': '', 'active': True},
        ]
        return context

    def form_valid(self, form):
        path = form.cleaned_data.get('path')
        f = form.cleaned_data.get('fileupload')
        with open(os.path.join(path, f.name), "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        self.success_url = reverse('system:sysfiles:list') + '?path=' + path
        return super().form_valid(form)


class FileDownloadView(SysfilesMixin, FormView):
    template_name = 'system/files_download.html'
    form_class = FileDownloadForm

    def get_initial(self):
        self.initial = super().get_initial()
        self.initial['path'] = self.request.GET.get('path')
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '从URL下载文件'
        context['path'] = self.request.GET.get('path')
        context['breadcrumb'] = [{
            'title': '文件列表',
            'href': reverse('system:sysfiles:list') + '?path=' + context['path'],
            'active': False},
            {'title': '下载文件', 'href': '', 'active': True},
        ]
        return context

    def form_valid(self, form):
        path = form.cleaned_data.get('path')
        url = form.cleaned_data.get('url')
        run = subprocess.run('wget -P {} "{}"'.format(path, url), shell=True, capture_output=True, encoding='utf-8')
        if run.returncode == 0:
            messages.success(self.request, "下载成功！")
            self.success_url = reverse('system:sysfiles:list') + '?path=' + path
        else:
            messages.warning(self.request, "下载不成功：{}".format(run.stderr.replace("\n", '</br>')))
            self.success_url = reverse('system:sysfiles:download') + '?path=' + path
        return super().form_valid(form)
