from django import forms
from .models import ChatMessages, Users, PersonalMessages, Mailing


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessages
        fields = ["message", "who_sent"]


class AuthForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput,
        }


class PersonalMessagesForm(forms.ModelForm):
    class Meta:
        model = PersonalMessages
        fields = ["message", "image", "recipient"]


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["message", "image"]


