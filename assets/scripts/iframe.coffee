define [
  'underscore'
  'views/player'
], (_, player)->
  current_song = window.current_song
  UPDATE_CURRENT_SONG_MSG = 0
  # This view is loaded from iframe
  window.addEventListener 'message', (event)->
    # console.log whatever
    # data, origin, source
    if _.isString event.data
      event.data = JSON.parse event.data
    if event.data.type == UPDATE_CURRENT_SONG_MSG
      current_song.set event.data.attributes
  , false

