from django.views.generic.edit import FormView

from .forms import InvokerForm


class InvokerView(FormView):
    template_name = 'scraper_invoker/invoker.html'
    form_class = InvokerForm
    success_url = 'waiting.html'

    def form_valid(self, form):
        pass
