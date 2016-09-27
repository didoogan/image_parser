
from django.conf.urls import url

from .views import InvokerView, ResultView


urlpatterns = [
    url(r'^$', InvokerView.as_view(), name='invoker'),
    url(r'^result/$', ResultView.as_view(), name='result'),
]
