# Copyright 2014, UFCG/Analytics
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django import shortcuts
from django.template import defaultfilters as filters
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import messages
from horizon import tables
from horizon.utils import functions

from openstack_dashboard.api.telemetry_api.telemetry_data import DataHandler

LOG = logging.getLogger(__name__)
HOSTS = []
HOSTS_ALL = []


class UpgradeFilterAction(tables.FilterAction):
    name = 'filter_upgrades'

    def filter(self, table, resources, filter_string):
        q = filter_string.lower()

        def comp(resource):
            if q in resource.type.lower():
                return True
            return False

        return filter(comp, resources)


class UpgradeTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    cpu_total = tables.Column('cpu_total', verbose_name=_('Total number of CPUs'))
    cpu_usage = tables.Column('cpu_usage', verbose_name=_('Number of CPUs used'))
    mem_total = tables.Column('memory_total', verbose_name=_('Total Memory (MB)'))
    mem_usage = tables.Column('memory_usage', verbose_name=_('Memory usage (MB)'))
    disk_total = tables.Column('disk_total', verbose_name=('Total Disk (GB)'))
    disk_usage = tables.Column('disk_usage', verbose_name=_('Disk used (GB)'))
    cpu_p = tables.Column('cpu_percentage', verbose_name=_('CPU (%)'))
    mem_p = tables.Column('memory_percentage', verbose_name=_('Memory (%)'))
    disk_p = tables.Column('disk_percentage', verbose_name=_('Disk (%)'))

    def get_object_id(self, obj):
        return "%s" % (obj.host)

    class Meta:
        name = "upgrades"
        verbose_name = _(" ")
#       table_actions = (UpgradeFilterAction,)
        multi_select = False


class FlavorTable(tables.DataTable):
    rec = tables.Column('name', verbose_name=_('Recommendation'))
    sugest = tables.Column('sugestion', verbose_name=_('Sugestion'))
    lose = tables.Column('lose', verbose_name=_('Lose (%)'))
    violation = tables.Column('violations', verbose_name=_('Violations (%)'))

    def get_object_id(self, obj):
        return "%s" % (obj.name)

    class Meta:
        name = "flavors"
        verbose_name = _('Flavors')


class StatusTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host'))
    status = tables.Column('status', verbose_name=_('Status'))

    def get_object_id(self, obj):
        return "%s" % (obj.host)

    class Meta:
        name = "status"
        verbose_name = _("Hosts Power Status")


class MigrationAllAction(tables.Action):
    name = "migration_button"
    verbose_name = _("Migrate All Host")
    verbose_name_plural = _("Migrate All Hosts")
    requires_input = False

    def handle(self, data_table, request, obj_ids):
         global HOSTS_ALL
         hosts_obj = []
         data_handler = DataHandler();

         if HOSTS_ALL:
             for host in HOSTS_ALL:
                 hosts_obj.append(self.table.get_object_by_id(host))
         else:
             for row in data_table.get_rows():
                 hosts_obj.append(self.table.get_object_by_id(row.cells['host'].data))
         
         for host in hosts_obj:
             for n in range(len(host.server)):
                 project = host.project[n]
                 host_name = host.endhost[n]
                 instance = host.server[n]

                 data_handler.migrate_to_host(project, host_name, instance)
         HOSTS_ALL = []

class RedefineAction(tables.BatchAction):
    name = "redefine_button"
    action_present = _("Redefine")
    action_past = _("Redefined")
    data_type_singular = _("Host")
    data_type_plural = _("Hosts")
    success_url = '/admin/recommendations'

    def action(self, request, obj_id):
        HOSTS.append(obj_id)

    def handle(self, table, request, obj_ids):
        action_success = []
        action_failure = []
        action_not_allowed = []

        for datum_id in obj_ids:
            datum = table.get_object_by_id(datum_id)
            datum_display = table.get_object_display(datum) or _("N/A")
            if not table._filter_action(self, request, datum):
                action_not_allowed.append(datum_id)
                LOG.info('Permission denied to %s: "%s"' %
                         (self._get_action_name(past=True).lower(),
                          datum_id))
                continue
            try:
                self.action(request, datum_id)
                self.update(request, datum)
                action_success.append(datum_id)
                self.success_ids.append(datum_id)
                LOG.info('%s: "%s"' %
                         (self._get_action_name(past=True), datum_id))
            except Exception as ex:
                # Handle the exception but silence it since we'll display
                # an aggregate error message later. Otherwise we'd get
                # multiple error messages displayed to the user.
                if getattr(ex, "_safe_message", None):
                    ignore = False
                else:
                    ignore = True
                    action_failure.append(datum_id)
                exceptions.handle(request, ignore=ignore)

        # Begin with success message class, downgrade to info if problems.
        success_message_level = messages.success
        if action_not_allowed:
            msg = _('You are not allowed to %(action)s: %(objs)s')
            params = {"action":
                      self._get_action_name(action_not_allowed).lower(),
                      "objs": functions.lazy_join(", ", action_not_allowed)}
            messages.error(request, msg % params)
            success_message_level = messages.info
        if action_failure:
            msg = _('Unable to %(action)s: %(objs)s')
            params = {"action": self._get_action_name(action_failure).lower(),
                      "objs": functions.lazy_join(", ", action_failure)}
            messages.error(request, msg % params)
            success_message_level = messages.info
        if action_success:
            msg = _('%(action)s: %(objs)s')
            params = {"action":
                      self._get_action_name(action_success, past=True),
                      "objs": functions.lazy_join(", ", action_success)}
            success_message_level(request, msg % params)
            for host in obj_ids:
                if host not in HOSTS_ALL:
                    HOSTS_ALL.append(host)
        return shortcuts.redirect(self.get_success_url(request))


class ResetMigrateAction(tables.Action):
    name = "reset_button"
    verbose_name = _("Reset")
    verbose_name_plural = _("Reset")
    requires_input = False

    def handle(self, data_table, request, obj_ids):
         global HOSTS_ALL
         HOSTS_ALL = []


def get_servers(zone):
    return zone.server


def get_names(zone):
    return zone.name


def get_endhosts(zone):
    return zone.endhost


def get_projects(zone):
    return zone.project


class MigrationTable(tables.DataTable):
    host = tables.Column('host',
                         verbose_name=_('Host'))
    server = tables.Column(get_servers,
                           verbose_name=_('Server ID'),
                           wrap_list=True, filters=(filters.unordered_list,))
    name = tables.Column(get_names,
                         verbose_name=_('Server Name'),
                         wrap_list=True,
                         filters=(filters.unordered_list,))
    end = tables.Column(get_endhosts,
                        verbose_name=_('New Host'),
                        wrap_list=True,
                        filters=(filters.unordered_list,))
    project = tables.Column(get_projects,
                            verbose_name=_("Project"),
                            wrap_list=True,
                            filters=(filters.unordered_list,))

    def get_object_id(self, obj):
        return "%s" % (obj.host)

    class Meta:
        name = "migration"
        verbose_name = _("Suggested Server Migrations")
        table_actions = (MigrationAllAction, RedefineAction, ResetMigrateAction,)
