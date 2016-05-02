from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db import transaction

from isasuk.meeting.models import Meeting
from .forms import AddEventForm
from ..meeting.models import Event
import json
import datetime

@transaction.atomic
@login_required
def calendar_view(request):
    form = AddEventForm()
    if request.user.details.role == 'member' and 'add' in request.POST:
      form = AddEventForm(request.POST)
      if form.is_valid():
        date = datetime.datetime.strptime(request.POST.get('date'), '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M')
        event = Event(
          title=request.POST.get('title'),
          date=date,
        )
        event.save()
        form = AddEventForm()
    elif request.user.details.role == 'member' and 'delete' in request.POST:
      event = Event.objects.get(id=request.POST.get('id'))
      event.delete()
    events = Event.objects.all().filter(date__gt=datetime.datetime.now()).order_by('date')
    return render_to_response('calendar/main.html',
        {
          'role': request.user.details.role,
          'events': events,
          'form': form,
        },
        context_instance=RequestContext(request),
      )

@transaction.atomic
@login_required
def events_view(request):
    meetings = Meeting.objects.all()
    e = Event.objects.all()#.filter(date__gt=datetime.datetime.now())
    events = []
    for meeting in meetings:
      events.append({
        'title': meeting.title,
        'start': meeting.date.isoformat(),
      })
    for event in e:
      events.append({
        'title': event.title,
        'start': event.date.isoformat(),
      })
    return HttpResponse(json.dumps(events))

