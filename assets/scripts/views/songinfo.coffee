#
# model - components | view in the model
#

define [
  'underscore'
  'backbone'
  'templates/sinfo'
], (_, Backbone, render_template)->

  class extends Backbone.View

    initialize: (options)->
      if not options.model?
        @model = require 'current_song'
      else
        @model = options.model

      @model.on 'change:sid', @render, @
      @model.on 'change:position', ->
        attributes = @model.serialize()
        @element('div.progress-play').css 'width': attributes.precentage
        @element('div.position').text(
          "#{attributes.position} / #{attributes.length}")
      , @

    element: _.memoize (selector)-> @$el.find(selector)

    render: ->
      @$el.html render_template(
        @model.serialize()
      )


