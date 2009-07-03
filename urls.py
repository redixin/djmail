from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'djmail.views.change_password'),
    (r'^admin/', include(admin.site.urls)),
)
