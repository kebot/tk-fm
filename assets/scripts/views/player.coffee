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
  'moment'
], (_, Backbone, soundManager, moment)->
  current_song = window.current_song

  class PlayerView extends Backbone.View
    initialize: ->
      @listenTo @model, 'change:sid', @changeSong
      @listenTo @model, 'change:playerposition', @onPositionChange
      @changeSong()
      @onPositionChange()
      @listenTo @model, 'play', =>
        @model.set 'started_at', moment.utc().valueOf()

    onPositionChange: ->
      position = @model.get('playerposition')
      if position
        @currentSong.setPosition(position)

    bindEvents: ->
      @currentSong.onplay = => @model.trigger 'play'

    play: ->
      @currentSong.play()

    changeSong: ->
      if not @model.get('sid')
        console.debug 'CurrentSong has not yet has a song!!!'
        return
      # onLoad the old song and destroy it.!!!
      @currentSong?.destruct()

      # get current time / Unix Offset(milliseconds)
      now = moment.utc().valueOf()
      position = @model.get('position') + now - @model.get('start_at')

      #currentTime = new Date()
      #tz = currentTime.getTime() + currentTime.getMilliseconds() / 1000
      #position = tz - @model.get('started_at')

      @currentSong = soundManager.createSound
        id: @model.get('sid')
        #url: "http://#{window._rock_host}/audio/#{@model.get('sid')}/#{@model.get('url')[7...]}"
        url: @model.get('url')
        position: position
        onplay: => @model.trigger 'play'
        onfinish: => @model.trigger 'finish'
        onstop: => @model.trigger 'stop'
        onresume: => @model.trigger 'resume'
        ondataerror: => console.error 'data error'
        whileplaying: => @model.set 'position', @currentSong.position
        #whileloading: => @model.set 'loaded', @currentSong.duration
        onload: => @model.set 'length', @currentSong.duration

      @bindEvents()
      @currentSong.play()

  new PlayerView model: current_song

