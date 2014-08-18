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


class SendMessageAction(tables.LinkAction):
    name = "send_message"
    verbose_name = _("Send Message")
    url = "horizon:admin:messages:message"
    classes = ("ajax-modal", "btn")


class UserFilterAction(tables.FilterAction):
    def filter(self, table, users, filter_string):
        """Naive case-insensitive search."""
        q = filter_string.lower()
        return [user for user in users
                if q in user.name.lower()
                or q in getattr(user, 'email', '').lower()]


class UsersTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_('User'))
    email = tables.Column('email',
                          verbose_name=_('Email'))
    id = tables.Column('id',
                       verbose_name=_('ID'))

#    def get_object_id(self, obj):
#        return "%s" % (obj.id)

#    def get_object_display(self, obj):
#        return "%s" % (obj.name)

    class Meta:
        name = "users"
        verbose_name = _("Users")
        row_actions = (SendMessageAction,)
        table_actions = (UserFilterAction,)


class ProjectsFilterAction(tables.FilterAction):
    def filter(self, projects, filter_string):
        q = filter_string.lower()

        def comp(projects):
            if q in users.type.lower():
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

#    def get_object_id(self, obj):
#        return "%s-%s" % (obj.project, obj.id)

    class Meta:
        name = "projects"
        verbose_name = _("Projects")
        row_actions = (SendMessageAction,)
        table_actions = (ProjectsFilterAction,)
        multi_select = False


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

#    def get_object_id(self, obj):
#        return "%s" % (obj.host)

    class Meta:
        name = "hosts"
        verbose_name = _("Hosts")
        row_actions = (SendMessageAction,)
        table_actions = (HostsFilterAction,)
        multi_select = False
