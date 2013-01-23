# Current_user

define ['backbone'], (Backbone)->
  class CurrentUser extends Backbone.Model
    isLogin: ->
      return @id == null

  return new CurrentUser

