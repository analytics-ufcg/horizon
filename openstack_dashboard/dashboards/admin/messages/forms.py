# Copyright 2014 UFCG - Analytics.
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

from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import messages

from messages.message_selection import MessageManager


class MessageUserForm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    subject = forms.CharField(label=_("Subject"))
    message = forms.CharField(widget=forms.widgets.Textarea(),
                                  label=_("Message"))

    def handle(self, request, data):
        messager = MessageManager();
        user_id = data.pop('id')

        try:
            messager.send_message(data['subject'], data['message'], user_id)
            messages.success(request,
                             _('Message for User has been sent successfully.'))
        except Exception:
            messages.error(request, _('Unable to send message for the user.'))

        return True
    
    
class MessageProjectForm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    subject = forms.CharField(label=_("Subject"))
    message = forms.CharField(widget=forms.widgets.Textarea(),
                                  label=_("Message"))

    def handle(self, request, data):
        messager = MessageManager();
        project_id = data.pop('id')
        
        try:
            messager.send_message_project(data['subject'], data['message'], project_id)
            messages.success(request,
                             _('Message for Project has been sent successfully.'))
        except Exception:
            messages.error(request, _('Unable to send message for the user.'))

        return True
        

class MessageHostForm(forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    subject = forms.CharField(label=_("Subject"))
    message = forms.CharField(widget=forms.widgets.Textarea(),
                                  label=_("Message"))

    def handle(self, request, data):
        messager = MessageManager();
        host_id = data.pop('id')
        
        try:
            messager.send_message_host(data['subject'], data['message'], host_id)
            messages.success(request,
                             _('Message for Host has been sent successfully.'))
        except Exception:
            messages.error(request, _('Unable to send message for the user.'))

        return True