from django.conf.urls.defaults import *
from views import *
from django.views.generic import ListView
from apps.profiles.models import Clinic

urlpatterns = patterns('',
    # Clinic
    url(r'^clinic/add/$', add_clinic, name="add_clinic"),
    url(r'^clinic/list/$', ListView.as_view(
        model=Clinic,
    ), name="list_clinic"),
    
    # Client
    url(r'^client/add/$', add_client_doctor, name="add_client"),
    url(r'^client/list/$', list_client, name='list_client'),
    url(r'^client/edit/(?P<client_id>\d+)/$', edit_client, name='edit_client'),
    
    # Doctor
    url(r'^doctor/add/$', add_doctor, name='add_doctor'),
    url(r'^doctor/list/$', list_doctor, name='list_doctor'),
    
    # Hostess
    url(r'^hostess/add/$', add_hostess, name='add_hostess'),
    url(r'^hostess/list/$', list_hostess, name='list_hostess'),
)