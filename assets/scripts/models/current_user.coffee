# Current_user

define ['backbone', 'underscore'], (Backbone, _)->

  class CurrentUser extends Backbone.Model
    isLogin: ->
      return not _.isEmpty(@id)

    serialize: ->
      _.extend @toJSON(), do =>
        if @isLogin()
          tail = "#{@get('id')}-#{
            parseInt(Math.random() * 100)
          }.jpg"

          iconl: "http://img3.douban.com/icon/ul" + tail
          icon: "http://img3.douban.com/icon/u" + tail
          is_login: true
        else
          return {is_login: false}

  return new CurrentUser

