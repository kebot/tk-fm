define 'collections/channel', [
  'backbone', 'models/song', 'models/current_user', 'underscore'
],(Backbone,  Song,           current_user,         _)->

  _groups = 'abcdefghijklmnopqrstuvwxyz' + '0123456789'
  randomString = (length)->
    output = ""
    while output.length < length
      output += _groups[_.random(0, _groups.length - 1)] 
    return output

  #params:
    #type: s、p、e、b、n、u、r
    #s: skip
    #p: playing <when play list is empty>
    #e: end <when one song ends>
    #b: ban <when song is marked as trash>
    #n: request a new playlist
    #u: unrate, r: rate
    #sid: current_sid
    #channel: current_channle
    #r: a random key. which.length() == 10
    #kbps: 192, 128, 64
    #from: mainsite
    # 'http://douban.fm/j/mine/playlist?type=n&sid=1408536&pt=0.9&channel=-3&pb=64&from=mainsite&r=1ae3ba797f'

  class ChannelListCollection extends Backbone.Collection
    initialize: (models, options)->
      if options.channel
        @channel_id = options.channel

    model: Song

    url: (options={})->
      return '/fm/mine/playlist?' + $.param(_.defaults(options, {
        'channel': @channel_id
        'type': 'n'
        # 'sid': ''
        'pt': 0.9
        'pb': 64
        'from': 'mainsite'
        'r': randomString(10)
      }))

    fetch: (options)->
      # available options
      # type: [spebnur]
      # sid: sid
      # @biubiubiu
      super _.extend(options, do =>
        if _.every(_.each(['type', 'sid'], (k)=>
          return _.has(options, k)
        ))
          return url: @url(_.pick(options, 'type', 'sid'))
        else
          return {}
      )

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
  RED_HEARTED = -3

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
        # default_channel = PERSONAl_CHANNEL
        default_channel = RED_HEARTED
      else
        default_channel = CHINESE_CHANNEL

      @history = new History()
      @channel = new Channel [], channel: default_channel

      @listenTo current_song, 'rate', @on_rate
      @listenTo current_song, 'finish', @on_finish

      @listenTo current_playlist, 'reset remove', =>
        if current_playlist.length > 0
          return true
        @moreSong()
        console.debug "Song in current_playlist:", current_playlist.toJSON()

    on_finish: =>
      console.debug "Finish playing the song -- ", current_song.toJSON()
      # when finish playing the song

    moreSong: =>
      # get more song from fm api.
      if @channel.length > 0
        current_playlist.create @channel.shift().toJSON()
        if current_song.isNew() or current_song.get('finish')
          current_song.trigger('finish')
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

