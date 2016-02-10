$(document).ready(function(){
  $('#datetimepicker').datetimepicker({
    'format': 'DD/MM/YYYY HH:mm',
    'sideBySide': true,
    'locale': moment.locale('sk')});

  $(".alert-success").fadeTo(2000, 500).slideUp(500, function(){});
})