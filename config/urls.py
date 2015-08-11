from django.conf.urls import include, url, patterns
from django.contrib import admin
import settings, os

admin.autodiscover()

js_info_dict = {
    'packages': (os.path.join(settings.APP_ROOT,'config'),)
}

urlpatterns = [
    url(r'^jsi8n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r'^change_language_ajax/$', 'users.views.change_language_ajax'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'users.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', 'users.views.index'),
    url(r'^register/$', 'users.views.register'),
    url(r'^register_action/$', 'users.views.register_action'),
    url(r'^login/$', 'users.views.login'),
    url(r'^login_action/$', 'users.views.login_action'),
    url(r'^account/$', 'users.views.account'),
    url(r'^logout/$', 'users.views.logout'),
    url(r'^update_account/$', 'users.views.update_account'),
    url(r'^scheduler/$', 'scheduler.views.scheduler'),
    url(r'^load_category_ajax/$', 'scheduler.views.load_category_ajax'),
    url(r'^update_category_ajax/$', 'scheduler.views.update_category_ajax'),
    url(r'^create_category_ajax/$', 'scheduler.views.create_category_ajax'),
    url(r'^delete_category_ajax/$', 'scheduler.views.delete_category_ajax'),
    url(r'^load_events_ajax/$', 'scheduler.views.load_events_ajax'),
    url(r'^create_events_ajax/$', 'scheduler.views.create_events_ajax'),
    url(r'^update_events_ajax/$', 'scheduler.views.update_events_ajax'),
    url(r'^delete_event_ajax/$', 'scheduler.views.delete_event_ajax'),
    url(r'^gantter/$', 'gantter.views.gantter'),
    url(r'^moneyer/$', 'moneyer.views.moneyer'),
    url(r'^load_moneyer/$', 'moneyer.views.load_moneyer'),
    url(r'^load_moneyer_category/$', 'moneyer.views.load_moneyer_category'),
    url(r'^create_moneyer/$', 'moneyer.views.create_moneyer'),
    url(r'^update_moneyer/$', 'moneyer.views.update_moneyer'),
    url(r'^delete_moneyer/$', 'moneyer.views.delete_moneyer'),
    url(r'^dashboard/$', 'users.views.dashboard'),
    url(r'^load_event_dashboard/$', 'scheduler.views.load_event_dashboard'),
    url(r'^load_dashboard_pie/$', 'moneyer.views.load_dashboard_pie'),
    url(r'^load_dashboard_line/$', 'moneyer.views.load_dashboard_line'),
]

if settings.DEBUG == False:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_ROOT}),
    )
