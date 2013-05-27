# The welcome view

define [
  'backbone'
  'models/current_user'
  'templates/room/welcome'
], (Backbone, current_user, render_template)->

  class extends Backbone.View

    initialize: (@options)->

    render: ->
      @$el.html render_template {
        current_user: current_user.serialize()
      }
      @el


