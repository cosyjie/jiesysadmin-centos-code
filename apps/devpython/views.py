import os
import re
import subprocess

from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.conf import settings

from apps.devlanguagemodule.views import DevLanguageContextMixin

from .forms import PythonInstallForm

from django.http import HttpResponse

from django.shortcuts import render


def import_iter(request):
    p = subprocess.Popen('cat /opt/install01.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    return render(request, 'system/xterm.html', {'content': 'd'})


class PythonContextMixin(DevLanguageContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'python'
        return context


def get_pyenv_installed():
    """获取pyenv的python版本"""
    rootdir = '/cosyjieserver/.pyenv/versions/'
    rlist = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if not os.path.islink(d) and os.path.isdir(d):
            rlist.append(file)
    rlist.sort(key=lambda x: tuple(int(v) for v in x.split(".")))
    return_list = {}
    for v in rlist:
        env_path = os.path.join(rootdir, v, 'envs')
        return_list[v] = []
        if os.path.exists(env_path):
            for env in os.listdir(env_path):
                return_list[v].append(env)
    return return_list


def get_pyenv_py_list():
    run = subprocess.run("pyenv install --list", shell=True, capture_output=True, encoding='utf-8')\
        .stdout.strip().split('\n')
    del run[0]
    return_list = []
    installed = get_pyenv_installed()
    for v in run:
        v_t = v.strip()
        v = v_t.split('.')
        if v[0].isdigit() and v[1].isdigit() and v[2].isdigit():
            if v_t not in installed:
                if (int(v[0]) == 2 and int(v[1]) >= 7 and int(v[2]) >= 5) or int(v[0]) >= 3:
                    return_list.append(v_t)
        # if re.match("^([3-9]\d|[3-9])(\.([1-9]\d|\d)){2}$", v):
        #     check = v.split('.')
        #     if v not in installed and int(check[1]) >= 3:
        #         return_list.append(v)
    return return_list


class PythonView(PythonContextMixin, TemplateView):
    template_name = 'devpython/python.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Python环境'
        context['menu'] = 'python'
        context['pylist'] = get_pyenv_installed()
        return context


class PythonDelView(PythonContextMixin, RedirectView):
    url = reverse_lazy('devpython:index')

    def get(self, request, *args, **kwargs):
        run = subprocess.run(
            'pyenv uninstall -f ' + self.kwargs.get('version'), shell=True, capture_output=True, encoding='utf-8'
        )
        if run.stderr:
            messages.warning(self.request, run.stderr)
        return super().get(request, *args, **kwargs)


class PythonInstallView(PythonContextMixin, FormView):
    template_name = 'devpython/python_install.html'
    form_class = PythonInstallForm
    success_url = reverse_lazy('devpython:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '安装Python'
        context['breadcrumb'] = [
            {'title': 'python环境', 'href': reverse('devpython:index'), 'active': False},
            {'title': '安装Python', 'href': '', 'active': True},
        ]
        context['pylist'] = get_pyenv_py_list()
        return context


def python_download(request):
    version = request.POST.get('version')
    website = request.POST.get('website')
    url = ''
    run_end = 0
    if website == 'python':
        url = 'https://www.python.org/ftp/python/'
    if website == 'aliyun':
        url = 'https://registry.npmmirror.com/-/binary/python/'
    if website == 'huaweicloud':
        url = 'https://mirrors.huaweicloud.com/python/{}/Python-{}.tar.xz'.format(version, version)
    if url:
        run_cmd = 'wget "{}" -O /cosyserver/.pyenv/cache/Python-{}.tar.xz'.format(url, version, version)
        run_end = subprocess.run(run_cmd, shell=True, capture_output=True, encoding='utf-8')
    return_dict = {'run_end': run_end.returncode, 'showprocess': ''}
    if run_end.stdout:
        return_dict['showprocess'] = run_end.stdout.replace('\n', '</br>')
    if run_end.stderr:
        return_dict['showprocess'] = run_end.stderr.replace('\n', '</br>')
    return JsonResponse(return_dict, safe=False)


def python_install_run(request):
    version = request.POST.get('version')
    v = version.split('.')
    if int(v[1]) >= 10:
        run_cmd = 'CPPFLAGS="$(pkg-config --cflags openssl11)" LDFLAGS="$(pkg-config --libs openssl11)" pyenv install ' \
                  + version
    else:
        run_cmd = 'pyenv install ' + version

    run_end = subprocess.run(run_cmd, shell=True, capture_output=True, encoding='utf-8')
    return_dict = {'run_end': run_end.returncode, 'showprocess': ''}
    if run_end.stdout:
        return_dict['showprocess'] = run_end.stdout.replace('\n', '</br>')
    if run_end.stderr:
        return_dict['showprocess'] = run_end.stderr.replace('\n', '</br>')

    return JsonResponse(return_dict, safe=False)
