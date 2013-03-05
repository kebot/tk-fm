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
      #@current_sid = null

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
      current_song = soundManager.createSound
        id: @model.get('sid')
        url: @model.get('url')
        #position: position
        #onplay: => @model.trigger 'play'
        onfinish: => @model.trigger 'finish'
        onstop: => @model.trigger 'stop'
        onresume: => @model.trigger 'resume'
        ondataerror: => console.error 'data error'
        whileplaying: => @model.set 'position', current_song.position
        onload: (success)=>
          console.debug @current_sid, ' :onload'
          if not success
            console.log 'load music error!'
            @model.trigger 'finish'
            return
          @model.set 'length', current_song.durationEstimate
          getCurrentPosition = =>
            now = time.current()
            position = (@model.get('position') or 0) \
                      + now - (@model.get('report_time') or now)
          setPositionIfLoaded = =>
            position = getCurrentPosition()
            if position > @model.get('length')
              @model.trigger 'finish'
              #@currentSong.stop()
              return false
            else if position < current_song.duration
              console.debug @current_sid, ' set position to - ', position
              current_song.setPosition(position)
              @model.once 'change:position', => @model.trigger 'play'
              return true
            else
              console.debug 'setPositionIfLoaded: do nothing'
              return false
          if not setPositionIfLoaded()
            current_song.options.whileloading = =>
              console.debug 'event: whileloading!'
              setPositionIfLoaded()
        onsuspend: => console.log 'suspend!!!!!!!!!!!'
      current_song.play()

  new PlayerView model: current_song

