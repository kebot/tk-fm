
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
});
