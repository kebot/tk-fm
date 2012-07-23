jQuery ->
  # effects
  jQuery('.dropdown-toggle').dropdown()

  #
  io = new Juggernaut
    host: document.location.hostname
    port: 8080

  io.on 'connect', -> console.log 'connected'
  io.on 'disconnect', -> console.log 'disconnected'
  io.on 'reconnect', -> console.log 'reconnecting'

  default_channel = 'channel1'
  console.log 'subscribing to ' + default_channel

  io.subscribe default_channel, (data)->
    $('#chat-bd').append(
      "<tr><td>#{data.author}</td><td>#{data.text}</td></tr>"
    )

  $('#postform').on 'submit', (e)->
    poster = $('#poster').val()
    message = $('#post-msg').val()
    io.publish default_channel, {author: poster, text: message}
    e.preventDefault()


