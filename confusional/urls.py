import pdb
from django.conf.urls import patterns, include, url
import confusional
from confusional.views import *
from confusional import views
from confusional.database.models import *
from confusional.database import models

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'confusional.views.home', name='home'),
    #url(r'^confusional/', include('confusional.foo.urls')),

    #Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
)

# Add in each model's views.
for m in dir(models):
    model = getattr(models, m)
    print m
    if '_meta' in dir(model) and 'app_label' in dir(model._meta):
        n = model._meta.module_name
        urlpatterns += patterns('',
            url(r'^%s/(?P<id>\d+)$' % (n),
                getattr(views, n)),
            url(r'^%s/' % (n),
                getattr(views, n)),
        )
