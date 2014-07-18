from messages.models import message_module

def get_message_by_recipient(recipient):
    ret = []
    for message in message_module.objects.all():
        if(message.recipient == recipient):
            ret.append(message)
    return ret
