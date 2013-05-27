
define [
  'underscore'
  'backbone'
  'templates/home'
  'models/current_song'
], (_, Backbone, render_template, current_song)->
  debug = window.debug && true

  RATE = 2
  SKIP = -1
  BAN = -2
  UNKNOW = 0

  class HomeView extends Backbone.View
    events:
      'click #rate': 'doRate'
      'click #ban' : 'doBan'
      'click #skip': 'doSkip'

    doRate: ->
      is_like = @model.get('like')
      if is_like
        @model.set 'like', UNKNOW
      else
        @model.set 'like', RATE
      false

    doBan: ->
      @model.set 'like', BAN
      false

    doSkip: ->
      @model.set 'like', SKIP
      false

    initialize: (options)->
      if not options.model?
        @model = require 'current_song'
      else
        @model = options.model

      @model.on 'change:like', =>
        $el = @$('#rate')
        if @model.get('like') > 0
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

    show: ->
      @$el.show()

    render: ->
      attributes = @model.serialize()
      @$el.html render_template(
        attributes
      )
      $('title').html "#{attributes.title} - TurkeyFM"
      @

  return new HomeView model: current_song

