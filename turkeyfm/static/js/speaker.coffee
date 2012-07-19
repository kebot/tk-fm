jQuery ->
  the_player = $('#player').get(0)
  notify_url = "/notify"

  playNextSong = (current_playing_song=Null)->
    $.getJSON notify_url, (r)->
      if r.list and r.list.length > 0
        sid = r.list.shift(0)
        $.getJSON "/song/#{sid}", (info)->
          the_player.src = info.url
          the_player.play()
          $.post "/notify",
            sid:sid
            action:'play'
      else
        window.setTimeout playNextSong, 1000

  $(the_player).on 'ended', playNextSong
  # playNextSong()
