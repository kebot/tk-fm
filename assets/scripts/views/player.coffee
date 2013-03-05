# this module wrap soundmanger whether in the iframe or 
define 'soundmanager-wrap', [
  'finish'
  'use'
  'jquery'
  'templates/iframeplayer'
], (finish, use, $, render_iframe)->
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
  current_song
  _
  Backbone
  soundManager
  time
)->
  class PlayerView extends Backbone.View
    initialize: ->
      @listenTo @model, 'change:sid', @changeSong
      @listenTo @model, 'change:playerposition', @onPositionChange

      @changeSong()
      @onPositionChange()

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

      # unload the old song and destroy it.!!!
      @currentSong?.destruct()

      # get current time / Unix Offset(milliseconds)
      @currentSong = soundManager.createSound
        id: @model.get('sid')
        url: @model.get('url')
        #position: position
        #onplay: => @model.trigger 'play'
        onfinish: => @model.trigger 'finish'
        onstop: => @model.trigger 'stop'
        onresume: => @model.trigger 'resume'
        ondataerror: => console.error 'data error'
        whileplaying: => @model.set 'position', @currentSong.position

        onload: (success)=>
          if not success
            console.log 'load music error!'
            @model.trigger 'finish'
            return

          @model.set 'length', @currentSong.durationEstimate

          getCurrentPosition = =>
            now = time.current()
            position = (@model.get('position') or 0) \
                      + now - (@model.get('report_time') or now)

          setPositionIfLoaded = =>
            position = getCurrentPosition()
            if position > @model.get('length')
              @model.trigger 'finish'
              @currentSong.stop()
              return false
            else if position < @currentSong.duration
              @currentSong.setPosition(position)
              @model.once 'change:position', => @model.trigger 'play'
              return true
            else
              return false

          if not setPositionIfLoaded()
            @currentSong.options.whileloading = => loaded_callback()

        onsuspend: => console.log 'suspend!!!!!!!!!!!'

      @currentSong.play()

  new PlayerView model: current_song

