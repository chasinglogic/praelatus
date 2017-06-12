/* Common functions used in Praelatus JS */

// Search a model returns a promise of the JSON response.
function searchModel(model_name, search) {
  console.log('sending','/api/v1/'+model_name+'?filter='+search);
  return fetch('/api/v1/'+model_name+'?filter='+search)
  .then(function(response) {
    return response.json();
  });
}

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}


var ticketPreview = {
  props: ['ticket'],
  template: '<h1>{{ ticket.key }}</h1>',
};
