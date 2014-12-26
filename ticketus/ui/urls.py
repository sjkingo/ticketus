from django.conf.urls import patterns, url

urlpatterns = patterns('ticketus.ui.views',
    url(r'^$', 'ticket_list', name='ticket_list'),
    url(r'^(?P<ticket_id>\d+)/$', 'ticket_page', name='ticket'),
    url(r'^(?P<ticket_id>\d+)/comment$', 'post_new_comment', name='post_new_comment'),
    url(r'^new/$', 'new_ticket', name='new_ticket'),
)
