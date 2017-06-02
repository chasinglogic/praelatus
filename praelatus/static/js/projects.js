function currentTicket() {
  return {
    key: 'test'
  };
}

ticketPreview.data = currentTicket;

new Vue({
  el: '#preview',
  components: {
    'ticket-preview': ticketPreview
  }
});


