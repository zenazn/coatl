from django.conf.urls.defaults import *
from coatl.registration import views

urlpatterns = patterns('',
    (r'^account', views.register_account),
    (r'^school', views.register_school),
    (r'^teams', views.register_teams),
    (r'^done', views.done),
    (r'', views.index),
)
