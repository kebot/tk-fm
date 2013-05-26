define [
  'backbone',
  'jquery',
  'underscore'
  'router'
  'models/current_user'
  'tweenMax'
], (
  Backbone
  $
  _
  router
  current_user
  TweenMax
)->
  # todo
  class extends Backbone.View
    events:
      'click [data-toggle=collapse]': 'toggleSidebar'
      'click ul.nav>li>a': 'triggerNavigate'

    initialize: (options)->
      @collection = new Backbone.Collection()

      @listenTo current_user, 'change', ->
        require ['templates/nav/user-info'], (render_template)->
          @$('#user-info').html(
            render_template(
              current_user.serialize()))

      current_user.trigger 'change'

    triggerNavigate: (event)->
      href = $(event.target).attr('href')
      Backbone.history.navigate(href, trigger: true)
      @toggleSidebar()
      return event.preventDefault()

    toggleSidebar: (event)->
      $nav = @$('.nav-collapse')
      $main = $('#app')
      wait = 0.5
      if $nav.css('left') == '0px'
        TweenMax.to($nav, wait, {left: '-70%'})
        TweenMax.to $main, wait, {'margin-left': 0}
      else
        TweenMax.to($nav, wait, {left: '0%'})
        TweenMax.to $main, wait, {'margin-left': $nav.width()}

    render: ->
      @$el.html render_template({
        title: 'turkey.fm'
        current_user: current_user.serialize()
      })
      @el

