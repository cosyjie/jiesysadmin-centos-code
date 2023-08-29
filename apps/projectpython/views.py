from django.views.generic.base import TemplateView
from apps.projectmodule.views import ProjectModuleContextMixin


class PythonContextMixin(ProjectModuleContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'pythonprojects'
        return context
    
    
