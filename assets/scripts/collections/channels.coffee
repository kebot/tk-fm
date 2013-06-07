define [
  'backbone',
  'underscore'
], (
  Backbone
  _
)->
  # search for channels: http://douban.fm/j/explore/search?query=%E6%B5%81%E8%A1%8C&start=0&limit=20
  # buildin channels --> http://l:5000/radio/channels
  # http://l:5000/radio/user_play_record

  class ChannelModel extends Backbone.Model
    idAttribute: 'channel_id'


  class extends Backbone.Collection


