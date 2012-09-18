from django import forms
from engineer.database.models import *
from django.contrib import admin

class EditParticipantForm(forms.ModelForm):
    class Meta:
        model=Participant

