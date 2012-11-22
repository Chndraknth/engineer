from django.contrib import admin
from django import forms
from confusional.database.models import *

class RoundInline(admin.TabularInline):
    """
    Creates a new form that gives round as inline in Event
    """
    model = Round
    extra = 3

class EventAdmin(admin.ModelAdmin):
    """Custom admin form for event
    """
    inlines = (
            RoundInline,
            )

class ParticipantForm(forms.ModelForm):
    """Custom Participant Admin Form
    """
    class Meta:
        model=Participant
        fields = ('slug', 'name', 'college_id', 'roll_no', 'email', 'fb_id')

    #def __init__(self, *args, **kwargs):
        #"""Neat hack to include only first rounds of all events
        #in the registration page
        #"""
        #super(ParticipantForm, self).__init__(*args, **kwargs)
        #allFirstRounds = []
        #allRounds = Round.objects.filter(number=1)
        #for round in allRounds:
            #allFirstRounds += [(round.id, round.__unicode__())]
        #rounds = self.fields['events'].widget
        #rounds.choices = allFirstRounds

class ParticipantAdmin(admin.ModelAdmin):
    """Custom Praticipant Admin
    """
    prepopulated_fields = {"slug": ("name",)}

class CollegeAdminForm(admin.ModelAdmin):
    model = College

class CollegeForm(forms.ModelForm):
    """Custom Participant Admin Form
    """
    class Meta:
        model=College

class CommitteeForm(forms.ModelForm):
    """Custom Participant Admin Form
    """
    class Meta:
        model=Committee

class ParticipationForm(forms.ModelForm):
    """Custom Participant Admin Form
    """
    class Meta:
        model=Participation


class EventForm(forms.ModelForm):
    """Custom Participant Admin Form
    """
    class Meta:
        model=Event

class RoundForm(forms.ModelForm):
    """Custom Participant Admin Form
    """
    class Meta:
        model=Round

class PrizeForm(forms.ModelForm):
    """Custom Participant Admin Form
    """
    class Meta:
        model=Prize

admin.site.register(
                    (
                        Round,
                        Committee
                    )
                   )
admin.site.register(
        Event, EventAdmin
        )
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(College)
admin.site.register(Participation)
admin.site.register(Prize)

