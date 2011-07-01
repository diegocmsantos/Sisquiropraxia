from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sisquiropraxia.views.home', name='home'),
    # url(r'^sisquiropraxia/', include('sisquiropraxia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^$', 'views.index'),
    
    (r'^accounts/', include('registration.backends.default.urls')),
    
    (r'^crm/', include('crm.urls')),
)
