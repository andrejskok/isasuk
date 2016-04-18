$(document).ready(function(){
  $('#calendar_container').fullCalendar({
    events: '/calendar/events',
    lang: 'sk',
  })

  $('#datetimepicker').datetimepicker({
    'format': 'DD/MM/YYYY HH:mm',
    'sideBySide': true,
    'locale': moment.locale('sk')});

  $(".alert-success").fadeTo(2000, 500).slideUp(500, function(){});

})