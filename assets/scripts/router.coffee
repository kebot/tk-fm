define ['jquery', 'backbone'], ($, Backbone)->
  # class Router extends Backbone.Router

  new class extends Backbone.Router
    routes:
      '': 'player'
      'account/login': 'login'

      'place/:name': 'switch_to_place'
      'song/search': 'search_song'

    index: ->
      # the main container
      require ['views/welcome'], (
        Welcome
      )->
        $('#app').html(
          new Welcome().render()
        )

