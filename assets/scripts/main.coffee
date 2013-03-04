###

      The TurkeyFM Project
    Copyright (C) 2013 Keith Yao
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###

define 'collections/channel', ['backbone', 'models/song'], (Backbone, Song)->
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
    model: Song
    url: ->
      '/fm/mine/playlist'
      #?type=n&sid=&pt=0.0&channel=0&from=mainsite&kbps=192&r=82e6b6a312'
    parse: (response)->
      if response.r == 0
        return response.song


define 'turkeyfm', [
  'underscore'
  'backbone'
  'collections/channel',
  'collections/current_playlist',
  'models/current_song',
  'models/current_user'
  #'templates/iframeplayer'
  'utils/io'
  'utils/time'
], (_
  Backbone
  Channel
  current_playlist
  current_song
  current_user
  #iframeplayer
  io
  time
)->
  channel = new Channel()

  class TurkeyFM
    constructor: ->
      _.extend this, Backbone.Events
      @listenTo current_song, 'finish', @nextSong
      @listenTo current_playlist, 'reset', =>
        console.debug 'Trigger current_playlist.reset, at `main.coffee`, line76'
        if _.isUndefined(current_song.id) and current_playlist.size() > 0
          this.nextSong()

      @listenTo current_song, 'play', =>
        if current_song.get('creater') == current_user.get('device_id')
          current_song.set 'report_time', time.current()
          current_song.save()

    nextSong: ->
      if current_playlist.length > 0
        # Remove and return the first song from collection
        current_song.clear(silent: true)
        current_song.set current_playlist.shift().toJSON()
        #current_song.save()

    joinroom: ->
      io.emit 'join', 'default_room', (resp)=>
        current_song.clear({silent: true})
        current_song.set(resp.current_song)
        current_playlist.reset(resp.song_list)
        if current_playlist.size() == 0
          channel.fetch success: ->
            # @TODO for future, will stop this, channel will always
            # auto-refresh, when the play-list is empty, every-user will
            # choose one song and add to the playlist.
            channel.each (model)->
              model.set('creater', current_user.get('device_id'))
              current_playlist.create model.toJSON()
            if _.isUndefined(current_song.id)
              # current_song is not playing
              current_playlist.trigger('reset')


    rock: ->
      #@initPlayer()
      require ['views/player'], (player)->

      # init the header-songinfo
      require ['views/songinfo'], (ViewSonginfo)->
        theview = new ViewSonginfo model: current_song
        $('#sinfo').append theview.el

      require ['views/songlist'], (songlist)->
        $('#main').append songlist.el

      io.on 'connect', @joinroom
      if io.socket.connected
        @joinroom()

show_login = ->
  require [
    'jquery'
    'backbone'
    'utils/ajax'
    'models/current_user'
  ], ($, Backbone, ajax, current_user)->
    ## if not login, then show the login form
    ajax.json '/account', (r)->
      if r.r == 0
        current_user.set r.user_info
      else
        require ['views/mod/login'], (mod_login)->
          $('body').append(mod_login.el)
          mod_login.show()

require [
  'turkeyfm'
  'jquery'
], (FM, $)->
  show_login()
  lets = new FM()
  # Let's rock, play the music!!!
  lets.rock()

