# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from engineer.database.models import *
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
from engineer.forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def menu(request, slug = ''):
    if slug:
        try:
            p = Participant.objects.get(slug__iexact = slug)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/register/'+slug)

    p = get_object_or_404(Participant, slug__iexact = slug)
    return render_to_response('menu.html', {'p': p, 'slug': slug})

def login_fail(request):
    return HttpResponseRedirect('/')

def admin_logout(request):
    if(request.user):
        logout(request)
    return HttpResponseRedirect(request.GET.get('next', None) or '/')

def admin_login(request):
    #messages.add_message(request, messages.INFO, 'You must log in')
    if(request.user):
        if(request.user.is_authenticated()):
            #messages.add_message(request,
                                #messages.INFO,
                                #'You are already logged in')
            return HttpResponseRedirect(request.GET.get('next', None) or '/')
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print 'logged in'
            return HttpResponseRedirect(request.GET.get('next', None) or '/')
        else:
            return HttpResponseRedirect('/login/fail')
    else:
        form = AdminLoginForm()
        c['form'] = form
    return render_to_response('form.html', c)



@login_required(login_url = '/login/admin')
def register(request, slug=''):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        p = Participant(slug = slug)
        form = RegistrationForm(request.POST, instance = p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/check/'+slug)
        else:
            c['form'] = form
    else:
        form = RegistrationForm()
        c['form'] = form
    return render_to_response('form.html', c)


def index(request):
    if(request.user):
        if(request.user.is_authenticated()):
            auth = True
        else:
            auth = False
    return render_to_response('index.html', locals())

def check_event_registration(request, slug=''):
    p = get_object_or_404(Participant, slug__iexact = slug)
    events = p.events.all()
    if(request.user.is_authenticated()):
        auth = True
    return render_to_response('check.html', locals())

@login_required(login_url='/login/admin')
def register_event(request, slug=''):
    c = {}
    c.update(csrf(request))
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
        c['form'] = form
    return render_to_response('form.html', c)
