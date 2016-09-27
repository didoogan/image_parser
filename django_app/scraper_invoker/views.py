import redis

from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from .forms import InvokerForm


class InvokerView(FormView):
    template_name = 'scraper_invoker/invoker.html'
    form_class = InvokerForm
    success_url = '/result/'

    def form_valid(self, form):
        query = form.cleaned_data.get('query')
        self.success_url = '/result/' + query
        # key = form.cleaned_data.get('query')
        # r = redis.StrictRedis()
        # images = r.smembers(key)
        return super(InvokerView, self).form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(InvokerView, self).get_context_data(**kwargs)
    #     r = redis.StrictRedis()
    #     images = r.smembers()
    #     context['images'] = images
    #     return context


class ResultView(TemplateView):
    template_name = 'scraper_invoker/result.html'

    def get_context_data(self, **kwargs):
        query = kwargs.get('query')
        context = super(ResultView, self).get_context_data(**kwargs)
        r = redis.StrictRedis()
        images = r.smembers(query)
        context['images'] = images
        return context
    #

