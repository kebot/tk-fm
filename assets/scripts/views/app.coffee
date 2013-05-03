
define [
  'underscore'
  'backbone'
  'templates/app'
], (_, Backbone, render_template)->
  debug = window.debug && true

  class AppView extends Backbone.View
    events:
      'click #rate': 'doRate'
      'click #ban' : 'doBan'
      'click #skip': 'doSkip'

    doRate: ->
      # @TODO set this to loading...
      @model.set 'like', not @model.get 'like'
      @model.trigger 'rate'
      false

    doBan: ->
      @model.trigger 'ban'

    doSkip: ->
      @model.trigger 'skip'

    initialize: (options)->
      if not options.model?
        @model = require 'current_song'
      else
        @model = options.model

      @model.on 'change:like', =>
        $el = @$('#rate')
        if @model.get('like')
          $el.removeClass('icon-heart-black').addClass('icon-heart-red')
        else
          $el.removeClass('icon-heart-red').addClass('icon-heart-black')

      @model.on 'change:sid', @render, @

      @model.on 'change:position change:length', ->
        attributes = @model.serialize()
        @$el.find('div.progress-bar').css 'width': attributes.precentage
        @$el.find('#playerposition').text(
          "#{attributes.position} / #{attributes.length}")
      , @

      if @model.get 'sid'
        @model.trigger('change:sid')

    element: _.memoize (selector)-> @$el.find(selector)

    render: ->
      attributes = @model.serialize()
      @$el.html render_template(
        attributes
      )
      $('title').html "#{attributes.title} - TurkeyFM"
      @


