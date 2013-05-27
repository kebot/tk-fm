define [
  'backbone',
  'jquery',
  'underscore'
  'templates/playlist/topsongs'
], (
  backbone
  $
  _
  render_template
)->
  new class extends Backbone.View
    show: -> @$el.show()

    render: ->
      $.getJSON '/j/topsongs', (json)=>
        @$el.html render_template(
          json
        )




