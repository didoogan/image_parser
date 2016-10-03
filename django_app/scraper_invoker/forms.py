import redis
import requests
import json

from django import forms


class InvokerForm(forms.Form):
    ENGINES = (
        ('google', 'Google'),
        ('yandex', 'Yandex'),
        ('instagram', 'Instagram'),
    )
    query = forms.CharField(max_length=100)
    engines = forms.MultipleChoiceField(choices=ENGINES, widget=forms.CheckboxSelectMultiple())

    def save(self):
        need_request = False
        r = redis.StrictRedis()
        query = self.cleaned_data.get('query')
        engines = {'google': False, 'yandex': False, 'instagram': False}
        engs = self.cleaned_data.get('engines')

        redis_result = r.hgetall(query)

        for engine in engs:
            # if not r.hgetall(query).get(engine, False):
            if redis_result.get(engine) in (None, '[]'):
                engines[engine] = True
                need_request = True
        if need_request:
            data = {'project': 'scraper', 'spider': 'image', 'question': query, 'google': engines['google'],
                    'yandex': engines['yandex'], 'instagram': engines['instagram']}
            requests.post("http://localhost:6800/schedule.json", data=data)
        return need_request
