from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$','django.contrib.auth.views.logout', name='logout'),
    (r'^admin/',  include(admin.site.urls)),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'django.conf'}),
    (r'', include('kenyakids.web.urls')),
#   For localization
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

#if not getattr(settings, "IS_PRODUCTION", None):
#    sitemedia = os.path.join(
#        os.path.dirname(__file__), 'sitemedia'
#        )
#    urlpatterns += patterns('',
#                            (r'^sitemedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': sitemedia }),
#                            )
