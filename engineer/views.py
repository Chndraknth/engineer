# Create your views here.
from django.core import serializers
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.context_processors import csrf
from engineer.database.models import * 
from django.forms.models import model_to_dict
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
from engineer.forms import *

def menu(request, slug = ''):
    p = get_object_or_404(Participant, slug__iexact = slug)
    return render_to_response('menu.html', {'p': p, 'slug': slug})

def index(requet):
    return render_to_response('layout.html')

def check_event_registration(request, slug=''):
    p = get_object_or_404(Participant.objects.filter(slug__iexact = slug))
    events = p.events.all()
    return render_to_response('check.html', locals())

def add_event_registration(request, slug=''):
    c = {}
    c.update(csrf(request))
    p = get_object_or_404(Participant.objects.filter(slug__iexact = slug))
    if request.method == 'POST':
        form = AddEventRegistrationForm(request.POST, instance = p)
        print request.POST
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/check/'+slug)
    else:
        form = AddEventRegistrationForm(instance = p)
        print form.fields['events'].widget
        c['form'] = form
    return render_to_response('form.html', c) 
