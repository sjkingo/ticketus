from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='ticket_list', permanent=False)),
    (r'^ticket/', include('ticketus.ui.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='account_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': 'ticket_list'},
            name='account_logout'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # Serve media files in development. Note Django automatically serves
    # static files as the staticfiles app is active in settings.py.
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
