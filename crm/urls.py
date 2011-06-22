from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^client/add/$', 'crm.views.add_client',name='add_client'),
    url(r'^client/list/$', 'crm.views.list_client',name='list_client'),
    url(r'^client/edit/(?P<client_id>\d+)$', 'crm.views.edit_client',name='edit_client'),
    
    url(r'^doctor/add/$', 'crm.views.add_doctor',name='add_doctor'),
    url(r'^doctor/list/$', 'crm.views.list_doctor',name='list_doctor'),
    
    url(r'^doctor/appointment/make/(?P<client_id>\d+)/$', 'crm.views.doctor_make_appointment',name='doctor_make_appointment'),
    url(r'^hostess/appointment/make/(?P<client_id>\d+)/$', 'crm.views.hostess_make_appointment',name='hostess_make_appointment'),
    
)
