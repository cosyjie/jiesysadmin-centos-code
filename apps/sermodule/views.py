from django.views.generic.base import ContextMixin


class SermoduleContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'sermodule'
        return context
