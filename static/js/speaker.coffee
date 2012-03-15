jQuery ->
  the_player = $('#player').get(0)
  notify_url = "/notify"
  current_song = {'sid':0}
  window.setInterval ->
    $.getJSON notify_url, (json)->
      if current_song.sid != json.song.sid
        current_song = json.song
        the_player.src = current_song.url
        the_player.play()
      else
        console.log '...No Changing...'
  ,1000
