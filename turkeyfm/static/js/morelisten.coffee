jQuery ->
  # init_project
  $('#hear-list').delegate ".one_song .btn-play", "click", (e)->
    sid = $(this).attr('data-sid')
    the_url = '/notify'
    $.post the_url, 'sid': sid

  # 
  current_song_info = 0

  # buttons
  btn_trash = $('#btn-trash')
  btn_like = $('#btn-like')
  i_like_icon = $("#btn-like i")
  btn_skip = $('#btn-skip')

  div_songinfo = $("#current-song-info .info")

  updateCurrentSong = ->
    $.getJSON '/notify', (current)->
      if current.song
        div_songinfo.html """ #{current.song.artist}:#{current.song.title}
          (<a href="http://www.douban.com/#{current.song.album}">
            #{current.song.albumtitle}
          </a>)"""
        i_like_icon.removeClass().addClass('icon-heart')
        current_song_info = current.song
      else
        div_songinfo.html """ Notplaying """

  tmpl_song_info = $("#tmpl-song-info").html()

  updateSongList = (the_list) ->
    r = $.parseJSON the_list
    tbody = Mustache.render tmpl_song_info, r
    $('#hear-list tbody').html tbody

  updateSongListForChannel = (channel=0) ->
    $.get "/channel/#{channel}", (list)->
      updateSongList(list)

  $('.choose-channel').click ->
    id = $(this).attr('data-id')
    updateSongListForChannel(id)
    return


  btn_like.click ->
    if i_like_icon.hasClass('icon-heart')
      $.post "/song/#{current_song_info.sid}/rate",{} ,(r)->
        console.log r
        i_like_icon.removeClass().addClass('icon-heart-red')
        updateSongList(r)
    else
      $.post "/song/#{current_song_info.sid}/unrate",{}, (r)->
        console.log r
        i_like_icon.removeClass().addClass('icon-heart')
        updateSongList(r)


  btn_trash.click ->
    $.post "/song/#{current_song_info.sid}/bye",{} ,(r)->
      console.log r
      updateSongList(r)


  btn_skip.click ->
    $.post "/song/#{current_song_info.sid}/skip",{} ,(r)->
      console.log r
      updateSongList(r)


  updateCurrentSong()
  updateSongListForChannel()

  $("#btn-refresh-song").click updateCurrentSong
