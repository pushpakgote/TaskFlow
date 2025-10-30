from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        # Skip login success message only
        if message_template == "account/messages/logged_in.txt":
            return
        super().add_message(request, level, message_template, message_context, extra_tags)
