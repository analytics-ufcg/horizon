from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from openstack_dashboard.dashboards.admin.availability import views

urlpatterns = patterns('openstack_dashboard.dashboards.admin.availability.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^host_availability$', views.HostsAvailabilityView.as_view(),name='host_availability'), 
)
