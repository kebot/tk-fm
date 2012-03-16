jQuery ->
  the_player = $('#player').get(0)
  notify_url = "/notify"

  song_list = []
  update_song_list = ->
    $.getJSON notify_url, (r)->
      song_list = r.list

  play_song = (sid) ->
    console.log "playing" + sid
    $.getJSON "/song/#{sid}", (r)->
      the_player.src = r.url
      the_player.play()
      $.post "/notify",
        sid:sid
        action:'play'
      , (pr)->
        song_list = pr.list

  $.getJSON notify_url, (r)->
      song_list = r.list
      window.setInterval ->
        console.log "."
        if the_player.paused or the_player.ended
          if song_list.length
            play_song(song_list[0])
          update_song_list()
      , 1000
