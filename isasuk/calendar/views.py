from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from isasuk.meeting.models import Meeting
import json
import datetime

@login_required
def calendar_view(request):
    return render_to_response('calendar/main.html',
        {},
        context_instance=RequestContext(request),
      )

def events_view(request):
    meetings = Meeting.objects.all()
    events = []
    for meeting in meetings:
      if not meeting.date:
        meeting.date = datetime.datetime.today()
      events.append({
        'title': meeting.title,
        'start': meeting.date.isoformat()
      })
    return HttpResponse(json.dumps(events))

