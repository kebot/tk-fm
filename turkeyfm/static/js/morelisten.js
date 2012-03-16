
jQuery(function() {
  return $('#hear-list').delegate(".one_song .btn-play", "click", function(e) {
    var sid, the_url;
    sid = $(this).attr('data-sid');
    the_url = '/notify';
    return $.post(the_url, {
      'sid': sid
    });
  });
});
