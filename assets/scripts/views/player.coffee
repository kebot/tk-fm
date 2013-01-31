###
  current_song

  change `id` will call :changeSong album and
  other meta-informations are related to id

  change `status` -- playing, paused

  `playerposition` -- try to keep sync in every player their playerposition
###
define [
  'underscore'
  'backbone',
  'soundmanager-ready'
], (_, Backbone, soundManager)->
  current_song = window.current_song

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

    bindEvents: ->
      @currentSong.onplay = => @model.trigger 'play'
      #for event in ['play', 'pause', 'stop']
        #@currentSong['on' + event] = do (event, @model)->
          #->
            #@model.trigger event

    play: ->
      @currentSong.play()

    changeSong: =>
      if not @model.get('sid')
        console.debug 'CurrentSong has not yet has a song!!!'
        return
      # onLoad the old song and destroy it.!!!
      @currentSong?.destruct()

      currentTime = new Date()
      tz = currentTime.getTime() + currentTime.getMilliseconds() / 1000
      position = tz - @model.get('started_at')

      @currentSong = soundManager.createSound
        id: @model.get('sid')
        url: "http://#{window._rock_host}/audio/#{@model.get('sid')}/#{@model.get('url')[7...]}"
        position: position
        onplay: => @model.trigger 'play'
        onfinish: => @model.trigger 'finish'
        onstop: => @model.trigger 'stop'
        onresume: => @model.trigger 'resume'
        ondataerror: => console.log 'data error'
        whileplaying: => @model.set 'position', @currentSong.position
        whileloading: => @model.set 'loaded', @currentSong.duration

      @bindEvents()
      @currentSong.play()

  new PlayerView model: current_song

