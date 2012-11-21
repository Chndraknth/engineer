# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.context_processors import csrf
from engineer.database.models import *
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
from engineer.forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from engineer.snippets.render_block import render_block_to_string


@login_required(login_url = '/admin/login')
def register(request, slug=''):
    if request.method == 'POST':
        p = Participant(slug = slug)
        form = RegistrationForm(request.POST, instance = p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/check/'+slug)
    else:
        form = RegistrationForm()
        form['slug']=slug
    return render(request, 'form.html', locals())

def index(request):
    return render(request, 'index.html', locals())

def welcome(request, slug=''):
    print request.session.get('participant')
    if(slug):
        p = Participant.objects.filter(slug__iexact=slug)
        if p:
            p=p[0]
            request.session['participant']=p.slug
        else:
            return HttpResponseRedirect('/register/'+slug)
    return render(request,"index.html", locals())

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        p = Participant.objects.filter(slug__iexact=username)
        if p:
            p = p[0]
            request.session['participant']=p.slug
            if request.POST.get('next', ''):
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect('/welcome/'+p.slug)
        else:
            return HttpResponseRedirect('/register/'+username)

def logout(request):
    del request.session['participant']
    return HttpResponseRedirect('/')

def check_event_registration(request, slug=''):
    p = get_object_or_404(Participant, slug__iexact = slug)
    user_events = p.events.all()
    if(request.user.is_authenticated()):
        auth = True
    return render(request, 'check.html', locals())

@login_required(login_url='/login/admin')
def register_event(request, slug=''):
    p = get_object_or_404(Participant, slug__iexact = slug)
    if request.method == 'POST':
        form = AddEventRegistrationForm(request.POST, instance = p)
        print request.POST
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/check/'+slug)
    else:
        form = AddEventRegistrationForm(instance = p)
        print form.fields['events'].widget
    return render(request, 'form.html', locals())

def ajax_event(request, event=''):
    return_string=""

