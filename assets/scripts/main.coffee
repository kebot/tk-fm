require.config
  baseUrl: '/static/scripts/'
  distUrl: '/static/dist'
__toString = Object.prototype.toString
__isArray = Array.isArray or (obj)-> __toString.call(obj) == '[object Array]'

bowerDefine = (package_name, deps, main_js, non_amd_callback=null)->
  if not __isArray deps
    non_amd_callback = main_js
    main_js = deps
    deps = []

  script_path = "http://localhost:5000/static/components/#{package_name}/#{main_js}"
  if non_amd_callback
    # define for non amd package
    src_name = "#{package_name}-src"
    # console.debug src_name, deps, script_path
    define src_name, deps, script_path
    define package_name, [src_name], non_amd_callback
  else
    # define for amd package
    define package_name, deps, script_path

bowerDefine 'jquery', 'jquery.js'
bowerDefine 'socket.io', 'dist/socket.io.js'
bowerDefine 'underscore', 'underscore.js', -> window._
bowerDefine 'backbone', ['jquery', 'underscore'], 'backbone.js', -> window.Backbone
bowerDefine 'handlebars', 'handlebars.runtime.js', -> window.Handlebars
bowerDefine 'nunjucks', 'browser/nunjucks.js', -> window.nunjucks
bowerDefine 'soundmanager', 'script/soundmanager2.js', -> window.soundManager

###
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
    #current_song.set msg

  room_name = 'room1'
  socket.emit 'join', room_name
###

require [
  'jquery'
  'backbone'
  'utils/ajax'
  'models/current_user'
], ($, Backbone, ajax, current_user)->
  ## if not login, then show the login form
  ajax.json '/account', (r)->
    if r.r == 0
      current_user.set r.user_info
    else
      require ['views/mod/login'], (mod_login)->
        $('body').append(mod_login.el)
        mod_login.show()

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

