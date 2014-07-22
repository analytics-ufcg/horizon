from messages.models import Message
import datetime


class MessageManager:
    def get_message_by_recipient(self, recipient):
        ret = Message.objects.filter(recipient=recipient)
        return ret

    def send_message(self, sender, recipient, subject, message):
        m = Message(sender=sender, recipient=recipient,
                    subject=subject,timestamp=datetime.datetime.now(),
                    message=message, read='F')
        m.save()

    def get_message_by_id(self, id):
        return Message.objects.filter(id=id)[0]
