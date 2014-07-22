from messages.models import Message
import datetime


class MessageManager:
    def get_message_by_recipient(self, recipient):
        ret = []
        for message in Message.objects.all():
            if(message.recipient == recipient):
                ret.append(message)
        return ret

    def send_message(self, sender, recipient, subject, message):
        m = Message(sender=sender, recipient=recipient, subject=subject,timestamp=datetime.datetime.now(), message=message, read='F')
        m.save()
