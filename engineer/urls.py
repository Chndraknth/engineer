from django.conf.urls import patterns, include, url
from engineer.views import *
from engineer import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'engineer.views.home', name='home'),
     #url(r'^engineer/', include('engineer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^slug/([a-zA-Z0-9\-]+)$', menu),
    url(r'^register/([a-zA-Z0-9\-]+)$', register),
    url(r'^logout$', admin_logout),
    url(r'^login/admin', admin_login),
    url(r'^login/fail', login_fail),
    url(r'^check/([a-zA-Z0-9\-]+)$', check_event_registration),
    url(r'^register_event/([a-zA-Z0-9\-]+)$', register_event),
    url(r'^$', index),

) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
