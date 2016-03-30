$(function() {
  $("#save-btn").on("click", function() {
      var ids = []
      $("#sortable2 li").each(function(index) {
          ids.push($(this).data("id"));
      });
      var data = {
          ids: JSON.stringify(ids),
          csrfmiddlewaretoken: $("#csrf").val(),
          meeting_id: $("#meeting_id").val(),
      }
      $.ajax({
        url: "/meeting/save/",
        method: "POST",
        data: data,
       })
      .done(function( data ) {
          data = JSON.parse(data);
          if (data.success) {
            window.location = '/meeting/upload_invitation/' + $("#meeting_id").val();
          }
      });
  })

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