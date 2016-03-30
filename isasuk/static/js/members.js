$(document).ready(function(){
  $.datepicker.setDefaults( $.datepicker.regional[ "" ] );
  $("#id_start").datepicker({dateFormat: 'dd/mm/yy',  'locale': moment.locale('sk')});
  $("#id_end").datepicker({dateFormat: 'dd/mm/yy'});
  $(".alert-success").fadeTo(2000, 500).slideUp(500, function(){
  });
  $(".edit").click(function(){$(this).parent().parent().next().toggle()});


  $('#add').click(function(){$('#add_form').toggle()})
})