
jQuery(function() {
  var btn_like, btn_skip, btn_trash, current_song_info, div_songinfo, i_like_icon, tmpl_song_info, updateCurrentSong, updateSongList, updateSongListForChannel;
  $('#hear-list').delegate(".one_song .btn-play", "click", function(e) {
    var sid, the_url;
    sid = $(this).attr('data-sid');
    the_url = '/notify';
    return $.post(the_url, {
      'sid': sid
    });
  });
  current_song_info = 0;
  btn_trash = $('#btn-trash');
  btn_like = $('#btn-like');
  i_like_icon = $("#btn-like i");
  btn_skip = $('#btn-skip');
  div_songinfo = $("#current-song-info .info");
  updateCurrentSong = function() {
    return $.getJSON('/notify', function(current) {
      if (current.song) {
        div_songinfo.html(" " + current.song.artist + ":" + current.song.title + "\n(<a href=\"http://www.douban.com/" + current.song.album + "\">\n  " + current.song.albumtitle + "\n</a>)");
        i_like_icon.removeClass().addClass('icon-heart');
        return current_song_info = current.song;
      } else {
        return div_songinfo.html(" Notplaying ");
      }
    });
  };
  tmpl_song_info = $("#tmpl-song-info").html();
  updateSongList = function(the_list) {
    var r, tbody;
    r = $.parseJSON(the_list);
    tbody = Mustache.render(tmpl_song_info, r);
    return $('#hear-list tbody').html(tbody);
  };
  updateSongListForChannel = function(channel) {
    if (channel == null) channel = 0;
    return $.get("/channel/" + channel, function(list) {
      return updateSongList(list);
    });
  };
  $('.choose-channel').click(function() {
    var id;
    id = $(this).attr('data-id');
    updateSongListForChannel(id);
  });
  btn_like.click(function() {
    if (i_like_icon.hasClass('icon-heart')) {
      return $.post("/song/" + current_song_info.sid + "/rate", {}, function(r) {
        console.log(r);
        i_like_icon.removeClass().addClass('icon-heart-red');
        return updateSongList(r);
      });
    } else {
      return $.post("/song/" + current_song_info.sid + "/unrate", {}, function(r) {
        console.log(r);
        i_like_icon.removeClass().addClass('icon-heart');
        return updateSongList(r);
      });
    }
  });
  btn_trash.click(function() {
    return $.post(current_sid);
  });
  updateCurrentSong();
  updateSongListForChannel();
  return $("#btn-refresh-song").click(updateCurrentSong);
});
