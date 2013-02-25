###
  current_song
  change `id` will call :changeSong album and
  other meta-informations are related to id
  change `status` -- playing, paused
  `playerposition` -- try to keep sync in every player their playerposition

  events for current_song
    finish: None
    playerposition: [report_time, position]
    play: None

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

      #@listenTo @model, 'play', =>
        #@model.set 'report_time', moment.utc().valueOf()
        #@model.save()

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
        onload: =>
          @model.set 'length', @currentSong.duration
          now = moment.utc().valueOf()
          position = (@model.get('position') or 0) \
                      + now - @model.get('report_time')
          if position > @model.get('length')
            @model.trigger 'finish'
            @currentSong.stop()
            return
          @currentSong.setPosition(position)
          @model.trigger 'play'
        #onsuspend: => console.log 'suspend!!!!!!!!!!!'

      @currentSong.play()

  new PlayerView model: current_song

