# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

from django.views.generic import TemplateView  # noqa
from django.shortcuts import render

import requests

class IndexView(TemplateView):
    template_name = 'admin/hosts/index.html'

    def get(self, request, *args, **kwargs):
        r = requests.get('http://localhost:9090/hosts')
        hosts_list = []
        if r.status_code == 200:
            hosts_list = r.json()['children']
        return render(request, self.template_name, {"hosts_list":hosts_list})
