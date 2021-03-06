
from django.conf.urls import url

from .views import InvokerView, ResultView, ResultSocketView
# from django.views.generic.base import TemplateView



urlpatterns = [
    url(r'^$', InvokerView.as_view(), name='invoker'),
    url(r'^result/(?P<query>\w+)$', ResultView.as_view(), name='result'),
    # url(r'^result_socket/$', TemplateView.as_view(template_name="scraper_invoker/result_socket.html")),
    # url(r'^result_socket/(?P<query>\w+)/(?P<engines>[\w,&]+)/(?P<need_request>\w+)/(?P<socket_engines>.*)$', ResultSocketView.as_view(), name='socket_result'),
    url(r'^result_socket/(?P<pk>[0-9a-z-]+)$', ResultSocketView.as_view(), name='socket_result'),
]
