import redis
import time
import json

import uuid

from django.utils.safestring import mark_safe


from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from .forms import InvokerForm
from .models import Query


class InvokerView(FormView):

    template_name = 'scraper_invoker/invoker.html'
    form_class = InvokerForm
    success_url = 'result_socket'

    def form_valid(self, form):
        r = redis.StrictRedis()
        query = form.cleaned_data.get('query')
        engines = '&'.join(form.cleaned_data.get('engines'))
        data = form.save()
        # self.success_url = '{}{}/{}/{}/{}'.format('/result_socket/', query, engines, data['need_request'], '&'.join(data['eng_for_websocket']))
        # self.success_url = '{}{}/{}/{}/{}'.format('/result_socket/', query, engines, data['need_request'], json.dumps(data['eng_for_websocket']))

        data = {'query': query, 'need_spiner': data['need_request'], 'engines': engines,
                  'socket_engines': json.dumps(data['eng_for_websocket'])}
        id = uuid.uuid1()
        r.hmset(id, data)
        self.success_url = 'result_socket/{}'.format(id)

        return super(InvokerView, self).form_valid(form)


class ResultSocketView(TemplateView):

    template_name = "scraper_invoker/result_socket.html"

    def get_context_data(self, **kwargs):
        r = redis.StrictRedis()
        context = super(ResultSocketView, self).get_context_data(**kwargs)
        id = kwargs.get('pk')
        query = r.hget(id, 'query')
        context['need_spiner'] = r.hget(id, 'need_spiner')
        engines = r.hget(id, 'engines').split('&')
        context['query'] = query
        socket_engines = r.hget(id, 'socket_engines')
        context['socket_engines'] = mark_safe(socket_engines)
        result = r.hgetall(query)
        if result:
            for engine in engines:
                # try:
                #     socket_engines = json.loads(socket_engines)
                # except TypeError:
                #     socket_engines = []
                # socket_engines = json.loads(socket_engines)
                if engine in socket_engines:
                    continue
                resp = result.get(engine, False)
                if resp:
                    # context[engine] = json.loads(result[engine])
                    context[engine] = json.loads(resp)
        return context


class ResultView(TemplateView):
    template_name = 'scraper_invoker/result.html'

