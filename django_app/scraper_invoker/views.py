import redis
import time
import json

from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from .forms import InvokerForm


class InvokerView(FormView):
    template_name = 'scraper_invoker/invoker.html'
    form_class = InvokerForm
    success_url = 'result_socket'

    def form_valid(self, form):
        query = form.cleaned_data.get('query')
        engines = '&'.join(form.cleaned_data.get('engines'))
        # self.success_url = '/result_socket/' + query
        need_request = form.save()
        self.success_url = '{}{}/{}/{}'.format('/result_socket/', query, engines, need_request)
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


class ResultSocketView(TemplateView):
    template_name = "scraper_invoker/result_socket.html"

    def get_context_data(self, **kwargs):
        r = redis.StrictRedis()
        context = super(ResultSocketView, self).get_context_data(**kwargs)
        query = kwargs.get('query')
        engines = kwargs.get('engines').split('&')
        context['query'] = query
        context['need_request'] = (kwargs.get('need_request'))
        result = r.hgetall(query)
        if result:
            result = {'google': json.loads(result['google']), 'yandex': json.loads(result['yandex']), 'instagram': json.loads(result['instagram'])}
            # context['result'] = result
            for engine in engines:
                context[engine] = result[engine]
        return context


class ResultView(TemplateView):
    template_name = 'scraper_invoker/result.html'

    # def get_context_data(self, **kwargs):
    #     time.sleep(5)
    #     query = kwargs.get('query')
    #     context = super(ResultView, self).get_context_data(**kwargs)
    #     r = redis.StrictRedis()
    #     images = r.smembers(query)
    #     images = map(json.loads, images)
    #
    #     context['google'] = []
    #     context['yandex'] = []
    #     context['instagram'] = []
    #
    #     for image in images:
    #         src = image.get('google_img', False)
    #         if src:
    #             context['google'].append(src)
    #             continue
    #
    #         src = image.get('yandex_img', False)
    #         if src:
    #             context['yandex'].append(src)
    #             continue
    #
    #         src = image.get('instagram_img', False)
    #         if src:
    #             context['instagram'].append(src)
    #             continue
    #
    #     return context


