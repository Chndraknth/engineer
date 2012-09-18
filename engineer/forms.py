from django import forms
from engineer.database import *
from django.contrib import admin

form EditParticipantForm(forms.ModelForm):

    class Meta:
        model=Participant

