from django import forms


class InvokerForm(forms.Form):
    ENGINES = (
        ('google', 'Google'),
        ('yandex', 'Yandex'),
        ('instagram', 'Instagram'),
    )
    query = forms.CharField(max_length=100)
    engines = forms.MultipleChoiceField(choices=ENGINES, widget=forms.CheckboxSelectMultiple())

    def invoke_scraper(self):
        pass
