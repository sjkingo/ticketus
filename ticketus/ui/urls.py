from django.conf.urls import patterns, url

urlpatterns = patterns('ticketus.ui.views',
    url(r'^(?P<ticket_id>\d+)/$', 'ticket_page', name='ticket'),
)
