from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^client/appointment/list/(?P<client_id>\d+)/$', list_appointment_client, name='list_appointment_client'),
    url(r'^doctor/appointment/make/(?P<client_id>\d+)/$', doctor_make_appointment, name='doctor_make_appointment'),
    url(r'^hostess/appointment/make/(?P<client_id>\d+)/$', hostess_make_appointment, name='hostess_make_appointment'),
)