from django import forms
from engineer.database.models import *
from django.contrib import admin
from django.forms import widgets

class AddEventRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddEventRegistrationForm, self).__init__(*args, **kwargs)
        print self.fields['events'].widget
        self.fields['events'].widget = widgets.CheckboxSelectMultiple
        print self
        
    class Meta:
        model = Participant
        fields = ('events', )


