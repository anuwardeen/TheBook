from django import forms
from .models import *
from django.contrib.auth.models import User

class CreateTopic(forms.ModelForm):

    class Meta:
        model = Topic
        fields = "__all__"

# class EditUser(forms.ModelForm):
#
#     class Meta:
#         model = User
#         fields = "__all__"
