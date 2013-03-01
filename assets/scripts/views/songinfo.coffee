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
      @model.on 'change:position change:length', ->
        attributes = @model.serialize()
        @$el.find('div.progress-play').css 'width': attributes.precentage
        @$el.find('div.position').text(
          "#{attributes.position} / #{attributes.length}")
        #console.log "#{attributes.position} / #{attributes.length}"
      , @

      if @model.get 'sid'
        @model.trigger('change:sid')

    element: _.memoize (selector)-> @$el.find(selector)

    render: ->
      @$el.html render_template(
        @model.serialize()
      )


