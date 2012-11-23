# Create your views here.
import pdb
import json
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, render
# from django.core.context_processors import csrf
from confusional.database.models import *
from confusional.database import *
from django.db import connection
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404, HttpResponse
#from confusional.forms import *
from confusional.database.admin import *
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

    return tabulate(results, False, fields)

def handler(m, request, id=None):
    table = {}
    cls = eval(m.title())

    forms = dict(
        college=CollegeForm,
        participant=ParticipantForm,
        event=EventForm,
        round=RoundForm,
        participation=ParticipationForm,
        committee=CommitteeForm,
        prize=PrizeForm,
    )

    if request.GET.get('action', None) or \
       request.POST.get('action', None):
        action = request.GET.get('action', None) or \
                 request.POST.get('action', None)
        res = False
        if action == 'delete':
            id = request.GET.get('id', None)
            if id:
                item = cls.objects.get(id=id)
                res = item.delete()
            return HttpResponse('')
        if action == 'exec':
            cur = connection.cursor()
            sql = request.GET.get('sql', None)
            if sql:
                cur.execute(sql)
                res = cur.fetchall()
                cur.close()
                header = [col[0].title() for col in cur.description]
                table = tabulate(res, False, header)
                return render(request, 'widgets/list.html', dict(list=table))
            

    table['url'] = '/%s/' % m
    table['name'] = m.title()

    if request.method == 'POST':
        form = forms[m](request.POST )
        #pdb.set_trace()
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Record created!")
            return HttpResponseRedirect("/%s/"%m)
        else:
            table['form'] = form
            print form.errors.values()
            messages.add_message(request, messages.ERROR, "Invalid data!")
            errors = []
            for e in form.errors:
                errors.append("%s: %s" %( e, " ".join(form.errors[e])))
            table['errors'] = errors
    else:
        table['form'] = forms[m]()
        form = table['form']

    if id:
        results = eval(m.title()).objects.filter(id=id)
        return render(
            request,
            'item.html',
            dict(list=tabulate(results),)
        )

    results = eval(m.title()).objects.all()
    table.update(tabulate(results, True, None, getattr(table, 'form', None)))
    if not getattr(table, 'form', None):
        table['form'] = forms[m]()

    return render(
        request,
        'list.html',
        dict(list=table)
    )


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

    if isinstance(fields[0], (str, unicode)):
        table['header'] = fields
        keys = fields

    else:
        for f in fields:
            table['header'].append(f.verbose_name)
            keys.append(f.name)
    if isinstance(results, tuple):
        table['body'] = results
    else:
        table['body'] = results.values_list()


    if form:
        table['form'] = form

    table['range'] = range(0, len(table['header']))
    table['fields'] = keys
    table['firstrow'] = zip(table['header'], table['body'][0])
    if editable:
        table['sql'] = str(getattr(results, 'query', ''))
    table['editable'] = ['', 'editable'][editable]

    return table

def index(request):
    proc = request.GET.get('action', None)
    date = '2012-11-22'
    venue = ''
   #if proc == 'proc':
   #    venue = request.GET.get('venue', '')
   #    date = '2012-11-22'
   #timetable = exec_proc('timetable', [date, venue], [Event._meta.get_field('name'), Round._meta.get_field('venue'), Round._meta.get_field('start_time')])
   #stats = exec_proc('event_details', [], ['Name', 'Rounds', 'Participants', 'Average score'])
   #recent = tabulate(Log.objects.all()[:10], False)
   #sentences = []
   #for r in recent['body']:
   #    _, iden, act, table = r
   #    sentences.append(["%s, %s was %s" % (table.title(), iden, act.lower())])
   #recent['header'] = ()
   #recent['body'] = sentences
    return render(request, 'index.html', locals())

def planner(request):
    return render(request, 'planner.html', locals())

def planner_data(request):
    results = []
    return HttpResponse(json.dumps(results), content_type='application/json')

college=lambda req, id=None: handler('college', req, id)
participant=lambda req, id=None: handler('participant', req, id)
participation=lambda req, id=None: handler('participation', req, id)
def event(req, id=None):
    if id:
        event = Event.objects.filter(id=id)
        rounds = Round.objects.filter(event_id=id)
        #pdb.set_trace()
        #rounds = Event.objects.filter(id=id)
        if event:
            return render(
                    req,
                    'event.html',
                    dict(
                        event=tabulate(event),
                        rounds=tabulate(rounds),
                        title=event[0].name
                    )
            )
    return handler('event', req, id)


round=lambda req, id=None: handler('round', req, id)
prize=lambda req, id=None: handler('prize', req, id)
committee=lambda req, id=None: handler('comittee', req, id)
def log(request, id=None):
    return render(request, 'list.html', dict(
        list=tabulate(Log.objects.all())))


