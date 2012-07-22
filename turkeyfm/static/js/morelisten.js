// Generated by CoffeeScript 1.3.3
(function() {

  jQuery(function() {
    var btn_like, btn_skip, btn_trash, current_song_info, div_songinfo, i_like_icon, tmpl_song_info, tmpl_waittinglist, updateCurrentSong, updateSongList, updateSongListForChannel, updateWaittingList;
    $('#hear-list').delegate(".one_song .btn-play", "click", function(e) {
      var sid, the_url;
      sid = $(this).attr('data-sid');
      the_url = '/notify';
      return $.post(the_url, {
        'sid': sid
      });
    });
    updateSongList = function(the_list) {
      var html, r;
      r = $.parseJSON(the_list);
      html = Mustache.render(tmpl_song_info, r);
      return $('#songlist-wrapper').html(html);
    };
    updateSongListForChannel = function(channel) {
      if (channel == null) {
        channel = 0;
      }
      return $.get("/channel/" + channel, function(list) {
        return updateSongList(list);
      });
    };
    $('.choose-channel').click(function() {
      var id;
      id = $(this).attr('data-id');
      updateSongListForChannel(id);
    });
    updateSongListForChannel();
    tmpl_waittinglist = $('#tmpl-waittinglist').html();
    updateWaittingList = function() {
      return $.getJSON('/songlist', function(list) {
        var html;
        html = Mustache.render(tmpl_waittinglist, list);
        return $('#songlist-wrapper').html(html);
      });
    };
    $('#btn-songlist').click(updateWaittingList);
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
      return $.post("/song/" + current_song_info.sid + "/bye", {}, function(r) {
        console.log(r);
        return updateSongList(r);
      });
    });
    btn_skip.click(function() {
      return $.post("/song/" + current_song_info.sid + "/skip", {}, function(r) {
        console.log(r);
        return updateSongList(r);
      });
    });
    updateCurrentSong();
    return $("#btn-refresh-song").click(updateCurrentSong);
  });

}).call(this);
