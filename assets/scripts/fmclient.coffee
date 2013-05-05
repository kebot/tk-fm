define 'collections/channel', [
  'backbone', 'models/song', 'models/current_user', 'underscore'
],(Backbone,  Song,           current_user,         _)->
  ###
  params:
    type: s、p、e、b、n、u、r
    s: skip
    p: playing <when play list is empty>
    e: end <when one song ends>
    b: ban <when song is marked as trash>
    n: request a new playlist
    u: unrate, r: rate
    sid: current_sid
    channel: current_channle
    r: a random key. which.length() == 10
    kbps: 192, 128, 64
    from: mainsite
  ###
  class ChannelListCollection extends Backbone.Collection
    initialize: (models, options)->
      if options.channel
        @channel_id = options.channel

    model: Song

    url: ->
      '/fm/mine/playlist'
      #?type=n&sid=&pt=0.0&channel=0&from=mainsite&kbps=192&r=82e6b6a312'
    fetch: (options)->
      super(options)

    parse: (response)->
      if response.r == 0
        return _.map response.song, (song)->
          song['creater'] = current_user.get('device_id')
          return song

define [
  'models/current_user'
  'models/current_song'
  'models/song'
  'collections/channel'
  'collections/current_playlist'
  'backbone'
  'underscore'
  'jquery'
], (current_user
  current_song
  Song
  Channel
  current_playlist
  Backbone
  _
  $
)->
  PERSONAl_CHANNEL = 0
  CHINESE_CHANNEL  = 1

  class HistoryItem extends Backbone.Model
    # request with history,
    # h=sid
    # type: /[psbr]/
    #   p: play
    #   s: skip
    #   b: ban
    #   r: rate
    idAttribute: 'sid'
    __str__: -> @get('sid') + ':' + @get('type')

  class History extends Backbone.Collection
    initialize: ->
    model: HistoryItem

  class FMClient
    constructor: ->
      _.extend this, Backbone.Events
      if current_user.isLogin()
        default_channel = PERSONAl_CHANNEL
      else
        default_channel = CHINESE_CHANNEL
      @history = new History()
      @channel = new Channel [], channel: default_channel

      @listenTo current_song, 'rate', @on_rate
      @listenTo current_song, 'finish', @on_finish

    on_finish: =>
      # when finish playing the song

    moreSong: =>
      # Pop one song from @channel to current playlist
      if @channel.length > 0
        # this is done by server-side
        current_playlist.create @channel.shift().toJSON()
        current_song.trigger('finish')
        ###
        if _.isUndefined(current_song.id)
          # current_song is not playing
          console.debug 'add song to playlist && no current_song, triger reset'
          current_playlist.trigger('reset')
        ###
      else
        @channel.fetch success: =>
          @moreSong()

    switch_channel: (cid)->
      @channel.channel_id = cid
      @channel.fetch()

    wrap_action = (type)->
      return (song)->
        attrs = _.pick song.toJSON(), 'sid', 'creater'
        attrs['type'] = action

    on_rate: (song)->
      sid = song.id
      if song.get('like')
        base_url = 'radio/like_song'
        type = 'r'
      else
        base_url = 'radio/unlike_song'
        type = 'u'

      $.getJSON "#{base_url}?sid=#{attrs.sid}", (response)->
        console.log response

    on_ban: (song)->
      # ban will request a new playlist

    #unrate:wrap_action('u')
    #ban: wrap_action('b')
    #skip: wrap_action('s')

    #unban: (song)->
      # NotImplementation
      #POST: 'http://douban.fm/j/song/657758/undo_ban'
      #'ck: J3AV'

  return new FMClient()


