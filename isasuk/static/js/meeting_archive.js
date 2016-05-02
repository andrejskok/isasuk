$(document).ready(function(){
  $("#id_start").datepicker({dateFormat: 'dd/mm/yy',  'locale': moment.locale('sk')});
  $("#id_end").datepicker({dateFormat: 'dd/mm/yy',  'locale': moment.locale('sk')});
})