#!/usr/bin/env coffee

# Global Namespace
App = {}

# ------- turkey-fm project -------
# ------- also a bubbler project demo ------


class mSong extends Backbone.Model
  urlRoot: '/api'

  idAttribute: "sid"

  url: ->
    if this.collection
      this.collection.url + '/' + this.get('sid')
    else
      this.urlRoot + '/song/' + this.get('sid')

  play: ->
    this.destroy {data: JSON.stringify({'playing': true})}

class mUser extends Backbone.Model
  url: ->
    return '/api/user/' + this.id

  validate: (attributes)->
    return null


class mBubbler extends Backbone.Model

class cChannel extends Backbone.Collection
  model: mSong
  url: ->
    '/api/channel/' + this.id

  parse: (r)->
    if r.r == 0
      return r.song
    else
      return []

  initialize: ->

# List for selected songs.
class cSelectedChannel extends cChannel
  url: '/api/selected'

class vCurrentSong extends Backbone.View

  initialize: ->
    this.template = Handlebars.compile $('#template-currentsonginfo').html()
    if this.model?
      this.model.on 'change', this.render, this

  #el: $('#current-song').get(0)

  events: {
    'click': 'toggle_pane'
  }

  toggle_pane: ->
    $('#channels').toggle()

  on_new_bubbler: (bubbler)=>
    console.log bubbler

  render: ->
    @$el.html(@template @model.toJSON())
    if @io_channel_name
      App.io.unsubscribe @io_channel_name
    @io_channel_name = 'bubbler-' + @model.get('sid')
    console.log "subscribing to #{@io_channel_name}"
    App.io.subscribe @io_channel_name, @on_new_bubbler


class vPlayer extends Backbone.View
  initialize: ->
    this.player_el = this.$('audio#player').get(0)
    if this.model?
      this.model.on 'change', this.change_song, this
    $player = $(this.player_el)
    $player.bind 'playing', @onplaying
    $player.bind 'ended',   @onended
    $player.bind 'playing', @onplaying
    $player.bind 'pause',   @onpause

  events: {
    #'error audio#player': 'onerror'
    #'ended audio#player': 'play_next'
    #'pause audio#player': 'onpause'
    #'playing audio#player': 'onplaying'
    'click button.btn-playpause': 'toggle_playing'
  }

  change_song: ->
    console.log 'song changed'
    if this.model.get('playing')
      stat = 'playing'
      audio_src = @model.get('local_url')
      @player_el.src = audio_src
      @player_el.play()
    else
      stat = 'pause'

    this.$('button.btn-playpause').html(stat)

  toggle_playing: (e)=>
    f_playing = this.model.get('playing')
    if not f_playing
      f_playing = true
    else
      f_playing = false
    @model.set({'playing': f_playing})
    if not @model.get('sid')
      this.play_next()

  notify: (extra)=>
    # $.post '/notify', _.extend(this.model.toJSON(), extra)
    this.log extra

  onplaying: =>
    this.model.play()
    this.notify {'state': 'playing'}

  onpause: =>
    this.notify {'state': 'pause'}

  onended: =>
    this.notify 'ended'
    this.play_next()

  onerror: (e)=>
    this.log('Error playing this song')
    this.play_next()

  play_next: (e)=>
    if this.model.get('playing')
      if first_model = this.collection.first()
        @model.set(first_model.toJSON())
        @model.collection = first_model.collection
        # $(this.player_el).attr('src', this.model.get('local_url'))
        # this.player_el.play()

  log: (message)=>
    console.log 'error: ' + message

class vLoginForm extends Backbone.View
  initialize: ->
    # this.onchange()
    this.model.on 'change', this.onchange, this

  events:
    'click .close': 'hide'
    'submit form' : 'submit'
    'click #login-submit': 'submit'

  onchange: ->
    if this.model.has('user_id')
      this.hide()

  show: ->
    this.$el.show()

  hide: ->
    this.$el.hide()

  submit: (e)-> # @ NotImplementException
    username = this.$('#username').val()
    password = this.$('#password').val()
    # console.log username
    # console.log password
    $.post '/api/login', {'username': username, 'password': password},
      this.onlogin
    e.preventDefault()

  onerror: (err)=>
    this.$('#login-info').removeClass().addClass('alert alert-error').html(err)

  onlogin: (r)=>
    if r.r == 0
    # callback function
      this.model.set r
      this.hide()
    else
      this.onerror r.err

class vBubblerAdd extends Backbone.View
  initialize: ->
    this.template = Handlebars.compile $('#template-songadd').html()
    this.model.on 'change', this.render, this
    # this.postform = new vPostForm el: $('#post-form-wrapper').get(0)

  events: {
    'click .lnk-issue' : 'display_postform'
  }

  display_postform: ->
    # this.postform.show()

  render: ->
    if this.model.has('icon')
      this.$el.html(this.template this.model.toJSON())

class vNewBubbler extends Backbone.View
  initialize: ->
    #@template = Handlebars.compile $('#template-')


class vChannelAndSongs extends Backbone.View
  initialize: ->
    this.render_channels()
    this.selected = if this.options.selected then this.options.selected \
      else new cSelectedChannel

    this.selected.on 'all', this.render_selected, this

    this.current_channel = if this.options.current_channel then this.options.current_channel \
      else new cChannel

    this.current_channel.on 'all', this.render_songs, this

    this.selected.fetch()

  events:{
    'click span.channel': 'load_channel'
    'click .close': 'close'

    'click .btn-add': 'add'
    'click .btn-up': 'up'
    'click .btn-delete': 'remove'

    'click span.selected': 'load_selected'
  }

  # add song to the list
  add: (e)=>
    sid = $(e.target).data('id')
    sid = parseInt sid
    this.selected.create {'sid': sid} #, url: this.selected.url

  up: (e)=>
    sid = $(e.target).data('id')
    # this.selected.remove {'sid': sid}, url: this.selected.url

  remove: (e)=>
    sid = $(e.target).data('id').toString()
    model = this.selected.where({'sid': sid})[0] #.destroy() #, url: this.selected.url
    model.destroy()

  close: =>
    this.$el.hide()

  load_selected: =>
    this.selected.fetch()

  load_channel: (e)=>
    channel_id = $(e.srcElement).data('id')
    this.current_channel.id = channel_id
    this.current_channel.fetch()
    # $.getJSON "/api/channel/#{channel_id}", this.render_songs

  render_channels: ->
    template = Handlebars.compile $('#template-channels').html()
    this.$('.modal-header').html template(window.channels)

  render_songs: ->
    template = Handlebars.compile $('#template-channel-songs').html()
    this.$('.modal-body').html template(this.current_channel.toJSON())

  render_selected: ->
    template = Handlebars.compile $('#template-channel-selected').html()
    this.$('.modal-body').html template(this.selected.toJSON())

$ ->
  current_user_model = new mUser 

  current_song_model = new mSong

  current_song_list = new cSelectedChannel

  loginform_view = new vLoginForm
    el: $('#login-form').get(0)
    model: current_user_model

  songadd_view = new vBubblerAdd {
    el: $('#song-add-wrapper').get(0)
    model: current_user_model
  }

  current_song_view = new vCurrentSong {
    el: $('#current-song').get(0)
    model: current_song_model
  }

  player_view = new vPlayer
    el: $('#player-wrapper').get(0)
    model: current_song_model
    collection: current_song_list
  # for debug
  window.player = player_view

  channel_view = new vChannelAndSongs
    el: $('#channels').get(0)
    selected: current_song_list

  # Controllers for Socket.Io(server side push)
  io = new Juggernaut
    host: document.location.hostname
    port: 8080

  io.on 'connect', -> console.log 'user connected'
  io.on 'disconnect', -> console.log 'user disconnected'
  io.on 'reconnect', -> console.log 'reconnected'

  console.log 'subscribing to channel current listening song.'

  # subscribe to
  io.subscribe 'current_song', (data)->
    current_song_model.set data

  io.subscribe 'selected', (r)->
    if r.change
      current_song_list.fetch()

  # Bubbler and bubblers.
  current_user_model.set window.current_user
  App.io = io

# Put it to global Name Space
window.App = App
