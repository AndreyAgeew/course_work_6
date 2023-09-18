from django import forms
from .models import Mailing, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'frequency', 'recipients', 'status']
        widgets = {
            'recipients': forms.CheckboxSelectMultiple,
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
