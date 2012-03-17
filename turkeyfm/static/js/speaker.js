
jQuery(function() {
  var notify_url, playNextSong, the_player;
  the_player = $('#player').get(0);
  notify_url = "/notify";
  playNextSong = function() {
    return $.getJSON(notify_url, function(r) {
      var sid;
      if (r.list && r.list.length > 0) {
        sid = r.list.shift(0);
        return $.getJSON("/song/" + sid, function(info) {
          the_player.src = info.url;
          the_player.play();
          return $.post("/notify", {
            sid: sid,
            action: 'play'
          });
        });
      } else {
        return window.setTimeout(playNextSong, 1000);
      }
    });
  };
  $(the_player).on('ended', playNextSong);
  return playNextSong();
  /*
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
          if the_player.paused or the_player.ended
            if song_list.length
              play_song(song_list[0])
            update_song_list()
        , 1000
  
    $.getJSON notify_url, (r)->
      song_list = r.list
  */
});
