define 'utils/io', [
  'socket.io'
  'models/current_user'
], (
  io,
  current_user
)->
  ns = io.connect '/room'
  ns.on 'connect', (data)->
    console.info 'io-connect'
    current_user.set('sessionid', ns.socket.sessionid)
  ns.on 'disconnect', -> console.info 'io-disconnect'
  return ns

# @TODO unuseful below
###
define 'utils/io-init', [
  'finish'
  'utils/io'
  'models/current_song'
  'collections/current_playlist'
], (
  finish,
  io,
  current_song,
  current_playlist
)->
  io.on 'init', (data)->
    current_song.clear({silent: true})
    current_song.reset(data.current_song)
    current_playlist.reset(data.song_list)
    finish ns
###

