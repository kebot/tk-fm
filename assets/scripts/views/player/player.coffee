# this module wrap soundmanger whether in the iframe or 
define 'soundmanager-wrap', [
  'finish'
  'jquery'
  'views/player/template'
], (finish, $, render_iframe)->
  use = {}
  use.iframe = true

  if use.iframe
    # http://www.ijusha.com/referer-anti-hotlinking/
    window.__iframe_html_string = render_iframe host: location.host
    window.onSoundMangerReady = (sm)->
      console.log 'soundManger in iframe ready'
      finish sm
      window.onSoundMangerReady = null
      window.__iframe_html_string = null

    iframe = $ '''<iframe
      id="turkey-player"
      src="javascript: parent.__iframe_html_string;"
      frameBorder="0"
      width="100"
      height="100"></iframe>'''
    $('body').append iframe
    iframe_window = iframe.get(0).contentWindow
  else
    require ['soundmanger'], (soundManger)->
      console.debug 'soundManger not in iframe'
      finish soundManger


define 'soundmanager-ready', [
  'finish'
  'soundmanager-wrap'
], (finish, soundManager)->
  soundManager.debugFlash = false
  # some setup for sound-manager2
  soundManager.setup
    allowScriptAccess: 'sameDomain'
    url: "http://#{location.host}/static/components/soundmanager/swf/soundmanager2_flash_xdomain/"
    useHTML5Audio: true
    preferFlash: false
    #SM2 is ready to play audio!
    onready: -> finish soundManager
    ontimeout: -> console.error 'soundManager is not ready'
    waitForWindowLoad: true
    debugMode: false


define [
  'models/current_song'
  'underscore'
  'backbone'
  'soundmanager-ready'
  'utils/time'
], (
  model
  _
  Backbone
  soundManager
  time
)->
  # play <-> pause . not to playing the song

  class PlayerView extends Backbone.View
    initialize: ->
      @listenTo @model, 'change:sid', @changeSong
      @listenTo @model, 'change:playerposition', @onPositionChange
      @changeSong()
      @onPositionChange()

      #@is_playing = false

    onPositionChange: ->
      position = @model.get('playerposition')
      if position
        @currentSong.setPosition(position)

    play: ->
      @currentSong.play()

    changeSong: ->
      if not @model.get('sid')
        console.debug 'CurrentSong has not yet has a song!!!'
        return

      if @current_sid
        # unload the old song and destroy it.!!!
        console.debug 'destroy sid:', @current_sid
        soundManager.destroySound @current_sid
        #@currentSong?.destruct()

      @current_sid = @model.get('sid')

      get_current_position = =>
        now = time.current()
        position = now - (@model.get('report_time') or now)

      current_song = soundManager.createSound
        id: @model.get('sid')
        url: @model.get('url')
        # unhandled methods
        onplay: => console.debug "Player: onplay"# @model.trigger 'play'
        onpause: => console.debug "Player: onpause"
        onresume: => console.debug "Player: onresume"#@model.trigger 'resume'
        ondataerror: => console.error 'data error'
        onfinish: => @model.trigger 'finish'
        onstop: => @model.trigger 'stop'
        whileplaying: =>
          @model.set 'position', current_song.position
          position = get_current_position()

          if get_current_position() > (
            current_song.durationEstimate or Infinity)

            return @model.trigger 'finish'

          distance = Math.abs(current_song.position - position)

          if distance < 100
            return

          console.debug "Position should be " + position +
            " but current_position is " + current_song.position

          for i in current_song.buffered
            if i.start < position < i.end
              return current_song.setPosition(get_current_position())

        onload: (success)=>
          @model.set 'length', current_song.durationEstimate
          @model.once 'change:position', =>
            @model.trigger 'play'

        onsuspend: => console.log 'suspend!!!!!!!!!!!'

      @model.on 'change:finish', ->
        current_song.pause()

      current_song.play()

  new PlayerView model: model

