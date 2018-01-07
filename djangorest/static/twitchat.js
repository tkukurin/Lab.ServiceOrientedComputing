$(function() {
  // When we're using HTTPS, use WSS too.
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var chatsock = new WebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    
  //const chatsock = new WebSocket(
  //  ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
  const messagesDiv = $("#chat-messages");
  //objDiv.scrollTop(objDiv.prop("scrollHeight"));

  chatsock.onmessage = message => {
      const data = JSON.parse(message.data)
      console.log(data);
    
      var chat = $("#chat-element").first().clone()
        .appendTo("#chat-element-list").removeClass('hidden');
      var body = chat.find("#chat-element-body")

      body.find("#chat-handle").text(data.handle)
      body.find("#msg-body").text(data.message)

      var details = chat.find("#chat-element-details")
      details.text(data.timestamp)
  };

  $("#chatform").on("submit", event => {
      chatsock.send(JSON.stringify({
          handle: 'xyz',
          message: $('#message').val(),
      }));
      $("#message").val('').focus();
      return false;
  });
});