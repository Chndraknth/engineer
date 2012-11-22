# Create your views here.
import pdb
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

    return tabulate(results, fields)

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
        prize=PrizeForm
    )

    if request.GET.get('action', None):
        action = request.GET.get('action')
        res = False
        if action == 'delete':
            id = request.GET.get('id', None)
            pdb.set_trace()
            if id:
                item = cls.objects.get(id=id)
                res = item.delete()
        return HttpResponse('')

    table['url'] = '/%s/' % m

    if request.method == 'POST':
        form = forms[m](request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Record created!")
        else:
            table['form'] = forms[m](request.POST)
            messages.add_message(request, messages.ERROR, "Invalid data!")
    else:
        table['form'] = forms[m]()

    if id:
        results = eval(m.title()).objects.filter(id=id)
        return render(
            request,
            'item.html',
            dict(list=tabulate(results),)
        )

    results = eval(m.title()).objects.all()
    table.update(tabulate(results))
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

college=lambda req, id=None: handler('college', req, id)
participant=lambda req, id=None: handler('participant', req, id)
participation=lambda req, id=None: handler('participation', req, id)
event=lambda req, id=None: handler('event', req, id)
round=lambda req, id=None: handler('round', req, id)
prize=lambda req, id=None: handler('prize', req, id)
committee=lambda req, id=None: handler('comittee', req, id)

