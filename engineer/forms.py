from django import forms
from django.shortcuts import get_object_or_404
from engineer.database.models import *
from django.contrib import admin
from django.forms import widgets

class AddEventRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddEventRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['events'].widget = widgets.CheckboxSelectMultiple(choices=self.fields['events'].widget.choices)
        self.fields['events'].help_text = 'Select as many events as you wish.'
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

class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['events'].widget = widgets.CheckboxSelectMultiple(choices=self.fields['events'].widget.choices)
        self.fields['events'].help_text = 'Select as many events as you wish.'
    class Meta:
        model = Participant
        fields = ('slug', 'name', 'college_id', 'roll_no', 'email', 'fb_id', 'events')

class AdminLoginForm(forms.Form):
    username = forms.CharField(label = "username")
    password = forms.CharField(label = "password", widget = widgets.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label = "")
    next = forms.CharField(label = 'next', widget = widgets.HiddenInput)
