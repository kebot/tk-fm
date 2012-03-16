
jQuery(function() {
  var current_song, notify_url, the_player;
  the_player = $('#player').get(0);
  notify_url = "/notify";
  current_song = {
    'sid': 0
  };
  return window.setInterval(function() {
    return $.getJSON(notify_url, function(json) {
      if (current_song.sid !== json.song.sid) {
        current_song = json.song;
        the_player.src = current_song.url;
        return the_player.play();
      } else {
        return console.log('...No Changing...');
      }
    });
  }, 1000);
});
