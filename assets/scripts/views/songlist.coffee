define [
  'backbone'
  'collections/current_playlist'
  'templates/playlist/song'
], (
  Backbone,
  playlist,
  template_song
)->

  class Song extends Backbone.View
    tagName: 'li'
    className: 'media'

    initialize: -> @listenTo @model, 'remove', @remove

    render: ->
      @$el.html template_song(@model.serialize())


  class List extends Backbone.View
    # define html node propery
    tagName: 'ul'
    className: 'media-list'
    id: 'current_playlist'

    initialize: (options)->
      @collection.on 'reset', (collection, options)=>
        collection.each @add_new
      , @

      @collection.on 'add', (model, collection, options)=>
        @add_new(model)
      , @

    add_new: (song_model)=>
      song_view = new Song model: song_model
      @$el.append(song_view.render())

  return new List({collection: playlist})

