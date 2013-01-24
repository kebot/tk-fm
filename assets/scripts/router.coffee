define ['backbone'], (Backbone)->
  # class Router extends Backbone.Router

  new class AppRouter extends Backbone.Router
    routes:
      # personal channel
      '/song/:sid': 'change_song'
      '/place/:name': 'switch_to_place'

    constructor: (options)->
      @options = options

    run: ->
      # be sure to call it after DOM is ready.
      result = Backbone.history.start({pushState: true})
      if result == true
        console.log 'successfully running the application!'

    registerApplication: (app)->
      # Source Code Pro for Powerline





