from django.views.generic import TemplateView  # noqa

from horizon import tabs
import json
from django.http import HttpResponse
from openstack_dashboard.dashboards.admin.availability import tabs as \
    availability_tabs

from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler
import requests, threading, ConfigParser, ast


class IndexView(tabs.TabView):
    tab_group_class = availability_tabs.AvailabilityTabs
    template_name = 'admin/availability/index.html'

class HostsAvailabilityView(TemplateView):
    template_name = 'admin/availability/host_availability.html'

    def get(self, request):
        return HttpResponse({})

