import re

from django import forms


class ChannelForm(forms.Form):
    channel_id = forms.RegexField(regex=re.compile(r'[A-Za-z0-9_\-]'))
    purpose = forms.CharField()
