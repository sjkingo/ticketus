from django.conf import settings
from django.conf.urls import patterns, include
from django.contrib import admin

urlpatterns = patterns('',
    (r'^ticket/', include('ticketus.ui.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        (r'^__debug__/', include(debug_toolbar.urls)),
    )

    # Serve media files in development. Note Django automatically serves
    # static files as the staticfiles app is active in settings.py.
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
