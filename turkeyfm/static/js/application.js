
jQuery(function() {
  var info, like, skip, songinfo, trash, updateCurrentSong;
  jQuery('.dropdown-toggle').dropdown();
  current - song - (info = 0);
  btn - (trash = $('#btn-trash'));
  btn - (like = $('#btn-trash'));
  btn - (skip = $('#btn-skip'));
  div - (songinfo = $("#current-song-info .info"));
  updateCurrentSong = function() {
    return $.getJSON('/notify', function(current) {
      return div - songinfo.html(" " + current.song.artist + ":" + current.song.title + "\n(<a href=\"http://www.douban.com/" + current.song.album + "\">\n  " + current.song.albumtitle + "\n</a>)");
    });
  };
  btn - trash.click(function() {
    return $.post(current - sid);
  });
  return updateCurrentSong();
});
