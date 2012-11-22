# Create your views here.
import pdb
from django.shortcuts import render_to_response, get_object_or_404, render
# from django.core.context_processors import csrf
from confusional.database.models import *
from confusional.database import *
from django.db import connection
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
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

def handler(m):
    def generic_handler(request, id=None):
        table = {}
        def get_all():
            results = Participant.objects.all()
            form = ParticipantForm()
            table = tabulate(results)
            table['form'] = form
            table['url'] = '/%s/' % m

            return table

        forms = dict(
            college=CollegeForm,
            participant=ParticipantForm,
            event=EventForm,
            round=RoundForm,
            participation=ParticipationForm,
            committee=CommitteeForm,
            prize=PrizeForm
        )

        if request.method == 'POST':
            form = forms[m](request.POST)
            if form.is_valid():
                form.save()
                table = get_all()
                table['msg'] = "Row created."
            else:
                table['msg'] = "Invalid data."
                table['form'] = form

        if id:
            results = getattr(locals(), m.title()).objects.filter(id=id)
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
    return generic_handler


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

college=handler('college')
participant=handler('participant')
participation=handler('participation')
event=handler('event')
round=handler('round')
prize=handler('prize')
committee=handler('committee')
