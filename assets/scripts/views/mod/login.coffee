define [
  'backbone'
  'jquery'
  'templates/login'
], (Backbone, $, render_template)->
  class Model extends Backbone.Model

  class LoginMod extends Backbone.View
    events:
      'click .close': 'hide'
      'submit form': 'submit'
      'click a.btn-primary': 'submit'

    initialize: ->

    submit: ->
      filter = (el)->
        $el = $(el)
        if $el.attr 'id'
          console.log $el.attr 'id', $el.val()
      [filter(element) for element in @$(':input')]

    show: ->
      $.getJSON '/account/new_captcha', (response)=>
        @$el.html render_template response
        @$('.modal').removeClass 'out'
        @$('.modal').addClass 'in'

    hide: ->
      @$('.modal').removeClass 'in'
      @$('.modal').addClass 'out'

  return new LoginMod()

