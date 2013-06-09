define [
  'backbone',
  'underscore'
  'moment'
  'utils/io'
  'utils/iosync'
], (
  Backbone
  _
  moment
  io
  iosync
)->
  
  # buildin events for this model:
  #   finish: when the player finish playing this song

  class CurrentSong extends Backbone.Model
    sync: iosync

    defaults:
      sid: ""
      picture: "http://img3.douban.com/pics/music/default_cover/lpic/music-default.gif"
      artist: ""
      albumtitle: ""
      title: ""

    idAttribute: 'sid'
    url: -> 'current_song'
    # // attribudes not given
    initialize: ->
      io.on 'current_song', (msg)=>
        console.log 'Receive current_song from server!!!', msg
        # if song-changed, clear previous attributes(
        #     player position,
        #     begin time...
        # )
        if not _.isUndefined(msg[@idAttribute]) and msg[@idAttribute] != @id
          @clear silent: true
        @set msg

    isEnd: -> (not @id) or @get('finish') 

    serialize: ->
      attributes = @toJSON()
      if @get('position') > 0 and @get('length') > 0
        attributes['precentage'] = "#{@get('position') / @get('length') * 100}%"
      else
        attributes['precentage'] = "0%"

      for key in ['position', 'length']
        if _.isUndefined(attributes[key]) or _.isNull(attributes[key])
          attributes[key] = ""
          continue
        m = moment(attributes[key])
        attributes[key] = "#{m.minute()}:#{m.second()}"

      attributes['like'] = attributes['like'] is not 0

      return attributes

  return new CurrentSong()

