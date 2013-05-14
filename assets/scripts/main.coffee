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


define 'turkeyfm', [
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
  class TurkeyFM
    constructor: ->
      _.extend this, Backbone.Events

    startListening: ->
      @listenTo current_song, 'play', =>
        current_song.save(
          _.extend(
            {'begin': true, 'report_time': time.current()},
            current_song.pick('position', 'sid'))
          , {patch: true})

      @listenTo current_song, 'finish', =>
        current_song.save({
          'finish': true,
          'sid': current_song.id
        }, {patch: true})


    joinroom: =>
      io.emit 'join', 'default_room', (resp)=>
        if _.isEmpty(resp.song_list)
          # add more song to songlist
          return FMClient.moreSong()

        if _.isEmpty(resp.current_song)
          return current_song.trigger('finish')

        current_song.clear({silent: true})
        current_song.set(
          resp.current_song
        )
        current_playlist.reset(resp.song_list)

        @startListening()

    rock: ->
      #@initPlayer()
      require ['views/player'], (player)->

      # init the header-songinfo
      require ['views/app'], (AppView)->
        theview = new AppView model: current_song
        $('#app').html theview.el

      #require ['views/songlist'], (songlist)->
        #$('#main').append songlist.el

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

