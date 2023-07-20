from django.views.generic.base import ContextMixin


class SystemMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'system'
        return context
