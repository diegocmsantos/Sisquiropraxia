from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^profiles/', include('sisquiropraxia.apps.profiles.urls')),
    (r'^agenda/', include('sisquiropraxia.apps.agenda.urls')),
    (r'^appointments/', include('sisquiropraxia.apps.appointments.urls')),
    (r'^payments/', include('sisquiropraxia.apps.payments.urls')),
    (r'^services/', include('sisquiropraxia.apps.service.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^$', 'views.index'),
    
    #url(r'^login/$', views.login, name='login'),
    
    (r'^accounts/', include('registration.backends.default.urls')),
)
