$(document).ready(function(){
  
    $('.selected_text').each(function(index, element){
      var d = $(element).children('div').first()
      if (d.length!==0){
        var total = 0;
        var divs = $(element).children('div').each(function(index, elem){
          console.log($(elem).height());
          $(elem).css({top: total});
          total += $(elem).height();
        })
      }
      var l = $(element).children('div').last()
      var height = 0
      if (l.length!==0){
        height = l.position().top + l.height()
      }
      $(element).css({'height': height+50})
    })

  $('#objections_target').on('mouseup', function handler(evt) {
    if (evt.type === 'mouseup') {
      $('#selected_text').html(getSelectionHtml())
      $('#hidden_input').val(getSelectionHtml())
      var d = $('#selected_text div').first()
      if (d.length!==0){
        var posd = d.position().top;
        var divs = $('#selected_text div').each(function(index, elem){
          var t = $(elem).position().top - posd;
          $(elem).css({top: t});
        })
      }

      var l = $('#selected_text div').last()
      var height = 0
      if (l.length!==0){
        height = l.position().top + l.height()
      }
      $('#selected_text').css({'height': height})
    } else {
      // drag
    }
  });

  function getSelectionHtml() {
    var html = "";
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i).cloneContents());
            }
            html = container.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange().htmlText;
        }
    }
    return html;
}

console.log(getSelectionHtml());


})