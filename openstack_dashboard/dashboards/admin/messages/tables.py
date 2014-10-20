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

from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class SendMessageUserAction(tables.LinkAction):
    name = "send_message_user"
    verbose_name = _("Send Message")
    url = "horizon:admin:messages:message_user"
    classes = ("ajax-modal", "btn-edit")


class UserFilterAction(tables.FilterAction):
    def filter(self, table, users, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [user for user in users
                if q in user.name.lower()
                or q in getattr(user, 'email', '').lower()]


class UsersTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_('User'))
    email = tables.Column('email', verbose_name=_('Email'))
    id = tables.Column('id', verbose_name=_('ID'))

    class Meta:
        name = "users"
        verbose_name = _("Users")
        row_actions = (SendMessageUserAction,)
        table_actions = (UserFilterAction,)
        multi_select = False


class SendMessageProjectAction(tables.LinkAction):
    name = "send_message_project"
    verbose_name = _("Send Message")
    url = "horizon:admin:messages:message_project"
    classes = ("ajax-modal", "btn-edit")
    
    
class ProjectsFilterAction(tables.FilterAction):
    def filter(self, table, projects, filter_string):
        q = filter_string.lower()

        def comp(projects):
            if q in users.name.lower():
                return True
            return False
        
        return filter(comp, projects)


class ProjectsTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_('Project'))
    description = tables.Column('description',
                          verbose_name=_('Description'))
    id = tables.Column('id',
                       verbose_name=_('ID'))

    class Meta:
        name = "projects"
        verbose_name = _("Projects")
        row_actions = (SendMessageProjectAction,)
        table_actions = (ProjectsFilterAction,)
        multi_select = False


class SendMessageHostAction(tables.LinkAction):
    name = "send_message_host"
    verbose_name = _("Send Message")
    url = "horizon:admin:messages:message_host"
    classes = ("ajax-modal", "btn-edit")


class HostsFilterAction(tables.FilterAction):
    def filter(self, hosts, filter_string):
        q = filter_string.lower()

        def comp(hosts):
            if q in users.type.lower():
                return True
            return False
        return filter(comp, hosts)


class HostsTable(tables.DataTable):
    id = tables.Column("id",
                         verbose_name=_('Host'))
    zone = tables.Column('zone',
                          verbose_name=_('Zone'))

    class Meta:
        name = "hosts"
        verbose_name = _("Hosts")
        row_actions = (SendMessageHostAction,)
        table_actions = (HostsFilterAction,)
        multi_select = False
