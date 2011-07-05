from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # Calendar
    url(r'^calendar/$', calendar, name='calendar'),
)