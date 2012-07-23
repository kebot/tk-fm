App = window.App

App.AppRouter = Backbone.Router.extend
  initialize: (options)->
    @app_view = new App.vApp {
      el: $('#app-container').get(0)
    }

  routes:
    '':      'board'
    '!/wall': 'wall'

  board: ->
    faker = window.faker
    template_bubitem = Handlebars.compile($('#template-bubitem').html())
    $el = $('.bublist')
    _.each faker.board, (bubdata)->
      $el.append template_bubitem(bubdata)

  wall: ->
    faker = window.faker
    # page Creating...
    # wall view.


