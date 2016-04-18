$(function() {
  $("#save-btn").on("click", function() {
      var ids = []
      var names = []
      $("#sortable2 li").each(function(index) {
          ids.push($(this).data("id"));
          names.push($(this).find('input').val())
      });
      var data = {
          ids: JSON.stringify(ids),
          csrfmiddlewaretoken: $("#csrf").val(),
          meeting_id: $("#meeting_id").val(),
          names:JSON.stringify(names),
      }
      $.ajax({
        url: "/meeting/save/",
        method: "POST",
        data: data,
       })
      .done(function( data ) {
          data = JSON.parse(data);
          if (data.success) {
            window.location = '/meeting/my_meetings/'// + $("#meeting_id").val();
          }
      });
  })

  $('#add_field').click(function() {
    $('#sortable2').append("<li class='ui-state-default' data-id='generic'>Názov<br><input class='form-control' type='text' /></li>");
  });

  $('.visibility').click(function(){
    elem = $(this).next();
    if (elem.hasClass('inv')) {
      elem.removeClass('inv');
      elem.addClass('v');
    } else {
      elem.removeClass('v');
      elem.addClass('inv');
    }
  })

  $( "#sortable1, #sortable2" ).sortable({
    connectWith: ".connectedSortable"
  }).disableSelection();
});