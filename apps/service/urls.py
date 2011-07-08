from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # Service
    url(r'^add/$', add_service, name="add_service"),
    url(r'^list/$', list_service, name='list_service'),
    
    # Table
    url(r'^table/add/$', add_table, name="add_table"),
    url(r'^table/list/$', list_table, name='list_table'),
    
    # Table Service
    url(r'^table_service/add/$', add_table_service, name="add_table_service"),
    url(r'^table_service/list/$', list_table_service, name='list_table_service'),
    
    # getting service price via ajax
    url(r'^price/ajax/(?P<client_id>\d+)/(?P<service_id>\d+)/$', service_price, name='service_price'),
)