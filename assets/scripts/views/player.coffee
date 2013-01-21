###
  current_song

  change `id` will call :changeSong album and
  other meta-informations are related to id

  change `status` -- playing, paused

  `playerposition` -- try to keep sync in every player their playerposition
###
define ['backbone',
  'soundmanager-ready'
], (Backbone, soundManager)->

  class PlayerView extends Backbone.View
    initialize: ->
      @listenTo @model, 'change:id', @changeSong
      @listenTo @model, 'change:playerposition', @onPositionChange

    onPositionChange: ->
      position = @model.get('playerposition')
      @currentSong.setPosition(position)

    changeSong: ->
      # onLoad the old song and destroy it.!!!
      @currentSong.destruct()
      @currentSong = soundManager.createSound
        id: @model.get('id')
        url: @model.get('url')
      song.play()

