define [
  'models/io'
  'moment'
], (IOModel, moment)->

  class Song extends IOModel
    idAttribute: 'sid'
    url: "/song/#{@id}"
    serialize: -> @toJSON()
    initialize: (attributes, options)->
      @set 'weight', moment.utc().valueOf()


