jQuery ->
  # init_project
  $('#hear-list').delegate ".one_song .btn-play", "click", (e)->
    sid = $(this).attr('data-sid')
    the_url = '/notify'
    $.post the_url, 'sid': sid
