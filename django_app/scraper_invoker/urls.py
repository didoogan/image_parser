
from django.conf.urls import url

from .views import InvokerView, ResultView
from django.views.generic.base import TemplateView



urlpatterns = [
    url(r'^$', InvokerView.as_view(), name='invoker'),
    url(r'^result/(?P<query>\w+)$', ResultView.as_view(), name='result'),
    url(r'^result_socket/$', TemplateView.as_view(template_name="scraper_invoker/result_socket.html")),
]
