from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class Availability(horizon.Panel):
    name = _("Availability")
    slug = "availability"


dashboard.Admin.register(Availability)
