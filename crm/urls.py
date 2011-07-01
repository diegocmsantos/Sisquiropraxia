from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('crm.views',
    # Client
    url(r'^client/add/$', 'add_client_doctor',name='add_client'),
    url(r'^client/list/$', 'list_client',name='list_client'),
    url(r'^client/edit/(?P<client_id>\d+)/$', 'edit_client',name='edit_client'),
    url(r'^client/appointment/list/(?P<client_id>\d+)/$', 'list_appointment_client',name='list_appointment_client'),
    
    # Doctor
    url(r'^doctor/add/$', 'add_doctor',name='add_doctor'),
    url(r'^doctor/list/$', 'list_doctor',name='list_doctor'),
    
    # Hostess
    url(r'^hostess/add/$', 'add_hostess',name='add_hostess'),
    url(r'^hostess/list/$', 'list_hostess',name='list_hostess'),
    
    url(r'^doctor/appointment/make/(?P<client_id>\d+)/$', 'doctor_make_appointment',name='doctor_make_appointment'),
    url(r'^hostess/appointment/make/(?P<client_id>\d+)/$', 'hostess_make_appointment',name='hostess_make_appointment'),
    
    # Calendar
    url(r'^calendar/$', 'calendar',name='calendar'),
)
