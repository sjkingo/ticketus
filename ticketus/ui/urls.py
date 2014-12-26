from django.conf.urls import patterns, url

urlpatterns = patterns('ticketus.ui.views',
    url(r'^$', 'ticket_list_all', name='ticket_list'),
    url(r'^user/(?P<username>[-_0-9a-zA-Z]+)/$', 'ticket_list_by_user', name='ticket_list_by_user'),
    url(r'^(?P<ticket_id>\d+)/$', 'ticket_page', name='ticket'),
    url(r'^(?P<ticket_id>\d+)/comment$', 'post_new_comment', name='post_new_comment'),
    url(r'^new/$', 'new_ticket', name='new_ticket'),
)
