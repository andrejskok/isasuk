$(document).ready(function(){
  $.datepicker.setDefaults( $.datepicker.regional[ "" ] );
  $("#group_start input").datepicker({dateFormat: 'dd/mm/yy',  'locale': moment.locale('sk')});
  $("#group_end input").datepicker({dateFormat: 'dd/mm/yy'});
  $("#leader_start input").datepicker({dateFormat: 'dd/mm/yy',  'locale': moment.locale('sk')});
  $("#leader_end input").datepicker({dateFormat: 'dd/mm/yy'});
})