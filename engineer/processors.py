from engineer.database.models import *
from engineer.forms import LoginForm

def events(request):
    return {'events': Event.objects.all()}

def participant(request):
    return {'participant': request.session.get('participant')}

def loginform(request):
    form = LoginForm()
    return {'loginform': form}
