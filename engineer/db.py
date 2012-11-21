# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from engineer.database.models import *
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
from engineer.forms import *
from django.core.exceptions import ObjectDoesNotExist

def participant(request):
    if request.method == 'POST':
        pass
    else:
        participants = Participant.objects.all()
        return render(request, "result.html", locals())


