# Create your views here.
import pdb
from django.shortcuts import render_to_response, get_object_or_404, render
# from django.core.context_processors import csrf
from confusional.database.models import *
from confusional.database import *
from django.db import connection
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
#from confusional.forms import *
from confusional.database.admin import ParticipantForm
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, authenticate, logout
# from django.contrib import messages
# from confusional.snippets.render_block import render_block_to_string

def exec_proc(proc, args, fields):
    cur = connection.cursor()
    cur.callproc(proc, args)
    results = cur.fetchall()
    cur.close()

    return tabulate(results, fields)


def tabulate(results, editable=True, fields=None, form=None):
    try:
        if not results or len(results) == 0:
            return dict(error="No results.")
    except:
        """A raw query result doesn't have len()"""
        return dict(error="No results.")
    keys = []
    table = dict(
        header = [],
        body = []
    )
    if not fields:
        fields = results[0]._meta.fields

    for f in fields:
        table['header'].append(f.verbose_name)
        keys.append(f.name)
    if isinstance(results, tuple):
        table['body'] = results
    else:
        table['body'] = results.values_list()

    table['range'] = range(0, len(table['header']))
    table['fields'] = keys
    table['firstrow'] = zip(table['header'], table['body'][0])
    table['sql'] = str(results.query)
    if form:
        table['form'] = form
        print "form: ", form.as_p

    table['editable'] = ['', 'editable'][editable]

    return table

def index(request):
    return render(request, 'index.html', locals())

def college(request, id=None):
    if id:
        results = College.objects.raw('select * from database_college')
        return render(
            request,
            'item.html',
            dict(list=tabulate(results))
        )
    else:
        results = College.objects.all()
        return render(
            request,
            'list.html',
            dict(list=tabulate(results),
                 )
        )


def committee(request, id=None):
    if id:
        results = Committee.objects.filter(id=id)
        return render(
            request,
            'item.html',
            dict(list=tabulate(results))
        )
    results = Committee.objects.all()
    return render(
        request,
        'list.html',
        dict(list=tabulate(results))
    )
    return render(request, 'index.html', locals())

def event(request, id=None):
    if id:
        results = Event.objects.filter(id=id)
        return render(
            request,
            'item.html',
            dict(list=tabulate(results))
        )
    results = Event.objects.all()
    return render(
        request,
        'list.html',
        dict(list=tabulate(results))
    )
    return render(request, 'index.html', locals())

def participant(request, id=None):
    table = {}
    def get_all():
        results = Participant.objects.all()
        form = ParticipantForm()
        table = tabulate(results)
        table['form'] = form
        table['formurl'] = '/participant/'

        return table

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            table = get_all()
            table['msg'] = "Row created."
        else:
            table['msg'] = "Invalid data."
            table['form'] = form

    if id:
        results = Participant.objects.filter(id=id)
        return render(
            request,
            'item.html',
            dict(list=tabulate(results),)
        )

    if not table:
        table = get_all()

    return render(
        request,
        'list.html',
        dict(list=table)
    )

def participation(request, id=None):
    if id:
        results = Participation.objects.filter(id=id)
        return render(
            request,
            'item.html',
            dict(list=tabulate(results))
        )
    results = Participation.objects.all()
    return render(
        request,
        'list.html',
        dict(list=tabulate(results))
    )
    return render(request, 'index.html', locals())

def prize(request, id=None):
    if id:
        results = Prize.objects.filter(id=id)
        return render(
            request,
            'item.html',
            dict(list=tabulate(results))
        )
    results = Prize.objects.all()
    return render(
        request,
        'list.html',
        dict(list=tabulate(results))
    )
    return render(request, 'index.html', locals())

def round(request, id=None):
    if id:
        results = Round.objects.filter(id=id)
        return render(
            request,
            'item.html',
            dict(list=tabulate(results))
        )
    results = Round.objects.all()
    return render(
        request,
        'list.html',
        dict(list=tabulate(results))
    )
    return render(request, 'index.html', locals())

