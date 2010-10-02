from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^registration/', include('registration.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'registration.views.index'),
)
