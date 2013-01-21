define ['backbone'], (Backbone)->
  class Song extends Backbone.Model
    url: "/song/#{@id}"


