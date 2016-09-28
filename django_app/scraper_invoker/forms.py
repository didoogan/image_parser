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
        query = self.cleaned_data.get('query')
        engines = {'google': True, 'yandex': False, 'instagram': False}
        engs = self.cleaned_data.get('engines')
        for engine in engs:
            engines[engine] = True
        data = {'project': 'scraper', 'spider': 'image', 'question': query, 'google': engines['google'],
                'yandex': engines['yandex'], 'instagram': engines['instagram']}
        requests.post("http://localhost:6800/schedule.json", data=data)
