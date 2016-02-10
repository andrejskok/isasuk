from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from isasuk.members.models import Group
from .forms import MeetingForm
from .models import Meeting
import datetime

def add_meeting_view(request):
  meetingform = MeetingForm(request=request)
  group = Group.objects.filter(member=request.user, is_chair=True)
  if request.user.is_superuser or len(group) > 0:
    successfully_added = False
    if 'add_meeting' in request.POST:
      print(request.POST['date'])
      meetingform = MeetingForm(request.POST, request=request)
      if meetingform.is_valid():
        add_meeting(request.POST.get('title'), request.POST.get('date'), request.POST.get('choices'))
        successfully_added = True
        meetingform = MeetingForm(request=request)
        return render_to_response(
          'meeting/add_meeting.html',
          {
            'form': meetingform,
            'successfully_added': successfully_added
          },
          context_instance=RequestContext(request)
          )
    return render_to_response(
      'meeting/add_meeting.html',
      {
        'form': meetingform,
      },
      context_instance=RequestContext(request)
      )
  else:
    return redirect('/meeting/meetings/')


def meetings_view(request):
  meetings = Meeting.objects.all()
  return render_to_response(
    'meeting/meetings.html',
    {
     'meetings': meetings,
    },
    context_instance=RequestContext(request)
  )

def add_meeting(title, date, group):
  date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M')
  meeting = Meeting(title=title, date=date, group=group)
  meeting.save()