import redis

from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from .forms import InvokerForm


class InvokerView(FormView):
    template_name = 'scraper_invoker/invoker.html'
    form_class = InvokerForm
    success_url = '/result/'

    def form_valid(self, form):
        # form.save()
        return super(InvokerView, self).form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(InvokerView, self).get_context_data(**kwargs)
    #     r = redis.StrictRedis()
    #     images = r.lrange('items', 0, 1)
    #     context['images'] = images
    #     return context


class ResultView(TemplateView):
    template_name = 'scraper_invoker/result.html'

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        r = redis.StrictRedis()
        images = r.lrange('items', 0, 1)
        context['images'] = images
        return context


