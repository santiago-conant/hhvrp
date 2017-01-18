from django.conf.urls import url

from . import views

app_name = 'problems'
urlpatterns = [
    url(r'^$', views.capture, name='capture'),
]
