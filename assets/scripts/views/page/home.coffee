
define [
  'underscore'
  'backbone'
  'views/page/home_template'
  'models/current_song'
  'tweenMax'
  'moment'
  'views/lyric'
], (_,
  Backbone
  render_template
  current_song
  tweenMax
  moment
  LyricView
)->
  debug = window.debug && true

  timing = (func, every=false, funcname="`fun_name`")->
    if _.isNumber(every)
      _first_time = false
      _count = 0
      return ->
        if _count < every
          if not _first_time
            _first_time = moment.utc().valueOf()
          _count += 1
        else
          console.info("#{funcname} is called #{every} times in #{
            moment.utc().valueOf() - _first_time
          } ms.")
          _first_time = false
          _count = 0
        func()
    else
      return func


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

      @model.on 'change:position change:length', _.throttle =>
          attributes = @model.serialize()
          TweenMax.to(@$el.find('div.progress-bar'), 
            0.1, 
            {
              width: attributes.precentage
            })
          @$el.find('#playerposition').text(
            "#{attributes.position} / #{attributes.length}")
        , 1000
      , @

      # bind subviews
      @lyric_view = new LyricView({
        model: @model
      })

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
      @lyric_view.setElement(@$el.find('#lyrics'))
      @lyric_view.render()

      $('title').html "#{attributes.title} - TurkeyFM"
      @

  return new HomeView model: current_song

