###
#   __  /_   _  ___
#   (  /) . /- / / )
#
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


define 'room', [
  'underscore'
  'backbone'
  'collections/current_playlist',
  'models/current_song',
  'models/current_user'
  'utils/io'
  'utils/time'
  'fmclient'
], (_
  Backbone
  current_playlist
  current_song
  current_user
  io
  time
  FMClient
)->
  new class TurkeyFM
    constructor: ->
      _.extend this, Backbone.Events

    startListening: ->
      @listenTo current_song, 'play', =>
        if current_song.get('report_time')
          return

        current_song.save(
          _.extend(
            {'begin': true, 'report_time': time.current()},
            current_song.pick('position', 'sid'))
          , {patch: true})

      # throttle version, it will called every 1000 times
      @listenTo current_song, 'finish', =>
        if current_song.get('finish')
          # you have reported that emmmm, i think so.
          return

        current_song.save({
          'finish': true,
          'sid': current_song.id
        }, {patch: true})
      #, 1000

      @listenTo current_song, 'change:like', =>
        current_song.save(
          current_song.pick('sid', 'like')
        , {patch: true})

    joinroom: (room_id)=>
      io.emit 'join', room_id, (resp)=>
        @startListening()
        if _.isEmpty(resp.song_list)
          # add more song to songlist
          FMClient.moreSong()

        if _.isEmpty(resp.current_song)
          return current_song.trigger('finish')

        current_song.clear({silent: true})
        current_song.set(
          resp.current_song
        )
        current_playlist.reset(resp.song_list)

    leaveroom: (room_id)=>
      # @Todo leave room.
      # (x) 1. destory the current_song and
      #     current_playlist(will be received from server)
      # 2. change current_room, show loading message.
      io.emit 'leave', room_id, (resp)=>
        console.debug 'user leave the room', room_id
        @stopListening()

    rock: (room_id)->
      require ['views/app'], (AppView)->
        theview = new AppView model: current_song
        $('#app').html theview.el


require [
  'utils/ajax'
  'models/current_user'
], (ajax, current_user)->
  ajax.json '/account', (r)->
    if r.r == 0
      current_user.set r.user_info

# join a random room
require [
  'underscore'
  'jquery'
  'router'
], (_, $, router)->
  
  # view based router
  _.each ['login', 'home', 'top'], (i)->
    router_name = i
    router.on 'route:' + i, ->
      require ['views/page/' + router_name], (pageView)->
        $('#pages>div').hide()
        $page = $('#page-' + router_name)
        if $page.length == 0
          $page = $(pageView.el)
          $page.attr 'id', 'page-' + router_name
          $('#pages').append $page
          pageView.render()
        pageView.show()

  $ ->
    require [
      'room'
      'views/player'
    ], (room, Player)->
      room.joinroom('whatever')

    require [
      'views/nav'
    ], (
      NavView
    )->
      aside = new NavView(
        el: $('#nav')
      )

    if Backbone.history.start({pushState: true})
      console.debug 'successfully run the application!'
    else
      console.debug 'No defined router defined for', location.href
      _.delay ->
        console.info 'Will navigate to / after 3 seconds!'
        Backbone.history.navigate '/', trigger: true
      , 3

