# Create your views here.
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.context_processors import csrf
from engineer.database.models import * 
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
from engineer.forms import *

def menu(request, slug = ''):
    p = get_object_or_404(Participant, slug__iexact = slug)
    form = EditParticipantForm(instance = p)
    return render_to_response('menu.html', {'p': p})

def index(requet):
    return render_to_response('layout.html')
