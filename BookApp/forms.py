from django import forms
from .models import *

class CreateTopic(forms.ModelForm):

    class Meta:
        model = Topic
        fields = "__all__"
