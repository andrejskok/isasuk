from django import template

register = template.Library()

attendance = {
  'present': '<i class="fa fa-check"></i>',
  'excused': 'Ospravedlnený',
  'absent': '<i class="fa fa-times"></i>',
}

@register.filter
def getattendancestatus(status):
  return attendance[status]