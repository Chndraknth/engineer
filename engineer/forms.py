from django import forms
from django.shortcuts import get_object_or_404
from engineer.database.models import *
from django.contrib import admin
from django.forms import widgets

class AddEventRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddEventRegistrationForm, self).__init__(*args, **kwargs)
        print self.fields['events'].widget
        self.fields['events'].widget = widgets.CheckboxSelectMultiple(choices=self.fields['events'].widget.choices)
        
    class Meta:
        model = Participant
        fields = ('events', )

class ProgressEventForm(forms.Form):
    select_from = forms.MultipleChoiceField(
            "Upgrade round",
            widget = widgets.CheckboxSelectMultiple,
            )

    def __init__(self, p, e):
        p = get_object_or_404(Participant, slug__iexact = p.slug)


