
jQuery(function() {
  var notify_url, play_song, song_list, the_player, update_song_list;
  the_player = $('#player').get(0);
  notify_url = "/notify";
  song_list = [];
  update_song_list = function() {
    return $.getJSON(notify_url, function(r) {
      return song_list = r.list;
    });
  };
  play_song = function(sid) {
    console.log("playing" + sid);
    return $.getJSON("/song/" + sid, function(r) {
      the_player.src = r.url;
      the_player.play();
      return $.post("/notify", {
        sid: sid,
        action: 'play'
      }, function(pr) {
        return song_list = pr.list;
      });
    });
  };
  return $.getJSON(notify_url, function(r) {
    song_list = r.list;
    return window.setInterval(function() {
      console.log(".");
      if (the_player.paused || the_player.ended) {
        if (song_list.length) play_song(song_list[0]);
        return update_song_list();
      }
    }, 1000);
  });
});
