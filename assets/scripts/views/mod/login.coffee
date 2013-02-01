define [
  'backbone'
  'jquery'
  'underscore'
  'templates/login'
  'utils/ajax'
  'models/current_user'
], (Backbone, $, _, render_template, ajax, current_user)->
  # backbone.formbind

  class LoginMod extends Backbone.View
    events:
      'click .close': 'hide'
      'submit form': 'submit'
      'click a.btn-primary': 'submit'

    initialize: ->
      @model = new Backbone.Model
        defaults:
          display: false

      @model.on 'change', @render

    render: => @$el.html render_template(@model.toJSON())

    new_captcha: -> $.getJSON '/account/new_captcha',
      (response)=> @model.set(response)

    submit: ->
      result = {}
      for element in @$(':input')
        $el = $(element)
        id = $el.attr('id')
        val = $el.val()
        console.debug id, val
        if id and val
          result[id] = val

      ajax.json '/account/login', 'POST', result, (result)=>
        if result.r == 0 and result.user_info
          current_user.set result.user_info
          @hide()
        else
          o = _.chain([
            [1011, 'captcha_error'],
            [1012, 'alias_error'],
            [1013, 'password_error'],
          ]).map((pair, index)->
            [code, name] = pair
            if code == result.err_no
              return [name, true]
            else
              return [name, false]
          ).object().extend(
            err_msg: result.err_msg
            captcha_id: false
          ).value()
          @model.set o
          @new_captcha()

    show: ->
      @model.set 'display': true
      @new_captcha()

    hide: -> @model.set 'display': false

  return new LoginMod()

