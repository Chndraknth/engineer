from django.contrib import admin
from django import forms
from engineer.database.models import *

class RoundInline(admin.TabularInline):
    """Creates a new form that gives round as inline in Event
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
    def __init__(self, *args, **kwargs):
        """Neat hack to include only first rounds of all events
        in the registration page
        """
        super(ParticipantForm, self).__init__(*args, **kwargs)
        allFirstRounds = []
        allRounds = Round.objects.filter(number=1)
        for round in allRounds:
            allFirstRounds += [(round.id, round.__unicode__())]
        rounds = self.fields['events'].widget
        rounds.choices = allFirstRounds

class ParticipantAdmin(admin.ModelAdmin):
    """Custom Praticipant Admin
    """
    form = ParticipantForm

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

