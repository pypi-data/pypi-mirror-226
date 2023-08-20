from django.urls import re_path

from mirrors.views import mirrors

urlpatterns = [
    re_path(r'^(?P<path>.*)$', mirrors),
]
