from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = patterns('ticketus.ui.views',
    url(r'^$', 'ticket_list', name='ticket_list'),
    url(r'^(?P<ticket_id>\d+)/$', 'ticket_page', name='ticket'),
    url(r'^(?P<ticket_id>\d+)/comment$', 'post_new_comment', name='post_new_comment'),
    url(r'^new/$', login_required(TemplateView.as_view(template_name='ui/new_ticket.html')), name='new_ticket'),
)
