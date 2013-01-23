define [
  'backbone'
  'jquery'
  'underscore'
  'templates/login'
  'utils/ajax'
  'models/current_user'
], (Backbone, $, _, render_template, ajax, current_user)->

  class LoginMod extends Backbone.View
    events:
      'click .close': 'hide'
      'submit form': 'submit'
      'click a.btn-primary': 'submit'

    initialize: ->

    submit: ->
      result = {}
      for element in @$(':input')
        $el = $(element)
        id = $el.attr('id')
        val = $el.val()
        console.log id, val
        if id and val
          result[id] = val
      ajax.json '/account/login', 'POST', result, (result)=>
        if result.r == 0 and result.user_info
          current_user.set result.user_info
          @hide()
        else
          # @TODO error handing
          console.log result

    show: ->
      $.getJSON '/account/new_captcha', (response)=>
        @$el.html render_template response
        @$('.modal').removeClass 'out'
        @$('.modal').addClass 'in'

    hide: ->
      @$('.modal').removeClass 'in'
      @$('.modal').addClass 'out'

  return new LoginMod()

