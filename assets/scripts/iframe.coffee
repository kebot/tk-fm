define [
  'underscore'
  'views/player'
], (
  _,
  player
)->
  current_song = window.current_song
  console.log 'hello'
  console.log player
  window.player = player


