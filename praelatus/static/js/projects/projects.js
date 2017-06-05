var project_key = 'TEST';
var defaultTicket = document.getElementById('ticket-list').children[0];
var converter = new showdown.Converter();

var preview = new Vue({
  el: '#preview',
  data: {
      key: '',
      summary: '',
      description: '',
      url: ''
  }
});


function loadPreview(tickEle) {
    var active = document.getElementsByClassName('active')
    if (active.length > 0) {
        active[0].className = 'ticket-stub';
    }

    tickEle.className += ' active'
    fetch('/api/v1/tickets/'+tickEle.id)
    .then(function(res) {
        return res.json();
    })
    .then(function(jsn) {
        preview.key = jsn.key;
        preview.summary = jsn.summary;
        preview.description = converter.makeHtml(jsn.description);
        preview.url = '/'+project_key+'/'+jsn.key;
    })
}

loadPreview(defaultTicket);
