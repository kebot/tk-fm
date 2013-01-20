require.config
  baseUrl: '/static/'
  distUrl: '/static/dist'
__toString = Object.prototype.toString
__isArray = Array.isArray or (obj)-> __toString.call(obj) == '[object Array]'

bowerDefine = (package_name, deps, main_js, non_amd_callback=null)->
  if not __isArray deps
    non_amd_callback = main_js
    main_js = deps
    deps = []

  script_path = "components/#{package_name}/#{main_js}"
  if non_amd_callback
    # define for non amd package
    src_name = "#{package_name}-src"
    define src_name, deps, script_path
    define package_name, [src_name], non_amd_callback
  else
    # define for amd package
    define package_name, deps, script_path

bowerDefine 'jquery', 'jquery.js'
bowerDefine 'socket.io', 'dist/socket.io.js'
bowerDefine 'underscore', 'underscore.js', -> window._
bowerDefine 'backbone', 'backbone.js', -> window.Backbone
bowerDefine 'nunjucks', 'browser/nunjucks.js', -> window.nunjucks
bowerDefine 'soundmanager', 'script/soundmanager2.js', -> window.soundManager

define 'soundmanager-ready', [
  'finish',
  'soundmanager'
], (finish, soundManager)->
  # some setup for sound-manager2
  soundManager.setup
    url: '/static/components/soundmanager/swf/'
    useHTML5Audio: true
    #SM2 is ready to play audio!
    onready: -> finish soundManager
    ontimeout: -> console.error 'soundManager is not ready'

require [
  'socket.io'
], (io)->
  socket = io.connect '/room'
  socket.on 'connect', -> console.info 'io-connect'
  socket.on 'disconnect', -> console.info 'io-disconnect'
  # custom events, current_song changed

  socket.on 'current_song', (msg)->
    console.info 'change current_song to', msg
    current_song.set msg

  # current_song


###
require [
  'soundmanager-ready'
], (soundManager)->
  # method one
  sound_biu = soundManager.createSound
    id: 'biu'
    url: 'http://bubbler.labs.douban.com/public/audio/biu3.mp3'
  sound_biu.play()
###


