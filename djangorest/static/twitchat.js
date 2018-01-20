$(function() {
  const supportsWebSockets = 'WebSocket' in window || 'MozWebSocket' in window;
  if (!supportsWebSockets) {
    $("body").innerHTML = "Sorry, your browser does not support WebSockets." + 
      "Keep up with the times.";
    return;
  }

  const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  const socket = new WebSocket(ws_scheme + '://' + window.location.host + "/chat");
  const messagesDiv = $("#chat-messages");
  
  socket.onmessage = message => {
    const data = JSON.parse(message.data);

    if (!data.message) {
      return;
    }
    
    const messageEl = document.createElement("p");
    messageEl.innerHTML = data.username + " says " + data.message;
    messagesDiv.append(messageEl);
  };

  $("#chatform").on("submit", event => {
    const message = $('#message').val();
    
    if (!message) {
      return;
    }
    
    socket.send(JSON.stringify(message));
    
    $("#message").val('').focus();
    return false;
  });
});