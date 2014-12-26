from django.conf.urls import patterns, url

from ticketus.ui.urls import urlpatterns

# Patch the ui's url patterns to include tag
urlpatterns += patterns('ticketus.tags.views',
    url(r'^tag/(?P<tag_name>[-_0-9a-zA-Z]+)/$', 'filter_by_tag', name='filter_by_tag'),
)
