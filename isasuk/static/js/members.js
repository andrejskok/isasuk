$(document).ready(function(){
  $("#id_start").datepicker({format: 'dd/mm/yyyy'});
  $("#id_end").datepicker({format: 'dd/mm/yyyy'});

  $(".alert-success").fadeTo(2000, 500).slideUp(500, function(){
  });
  $(".edit").click(function(){$(this).parent().parent().next().toggle()});
})