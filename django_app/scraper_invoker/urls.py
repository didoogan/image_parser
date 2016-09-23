
from django.conf.urls import url
from django.contrib import admin

from .views import InvokerView

urlpatterns = [
    url(r'', InvokerView.as_view(), name='invoker'),
]
