#!
# * CoffeeScript rewrite for iobind
# Do Not Rewrite The Original Backbone Model AMD Support
#
# @TODO pull request to original project!
# ===================================
#
#   Origin written by ---
# * backbone.iobind - Model
# * Copyright(c) 2011 Jake Luer <jake@alogicalparadox.com>
# * MIT Licensed
#

define ['backbone', 'utils/iosync'], (Backbone, iosync)->
  VERSION = "0.4.4"

  class IOModel extends Backbone.Model
    sync: iosync

  ###
  # .ioBind(event, callback, [context])

  Bind and handle trigger of socket.io events for models.

  /// Guidelines

  Do NOT bind to reserved backbone events, such as `change`, `remove`, and `add`
  Proxy these events using different event tags such as `update`, `delete`, and
  `create`.

  The socket.io socket must either exist at `window.socket`, `Backbone.socket`,
  or `this.socket` or it must be passed as the second argument.

  /// Example

  Model definition has url: `my_model`
  Model instance has id: `abc123`

  //// Create a new bind (client-side):

  model.ioBind('update', window.io, this.updateView, this);

  //// Send socket.io message (server-side)

  socket.emit( 'my_model/abc123:update', { title: 'My New Title' } );

  @name ioBind
  @param {String} eventName
  @param {Object} io from active socket.io connection (optional)
  @param {Function} callback
  @param {Object} context (optional) object to interpret as this on callback
  @api public
  ###

  IOModel::ioBind = (eventName, io, callback, context) ->
    ioEvents = @_ioEvents or (@_ioEvents = {})
    globalName = @url() + ":" + eventName
    self = this
    if "function" is typeof io
      context = callback
      callback = io
      io = @socket or window.socket or Backbone.socket
    event =
      name: eventName
      global: globalName
      cbLocal: callback
      cbGlobal: ->
        args = [eventName]
        args.push.apply args, arguments_
        self.trigger.apply self, args

    @bind event.name, event.cbLocal, (context or self)
    io.on event.global, event.cbGlobal
    unless ioEvents[event.name]
      ioEvents[event.name] = [event]
    else
      ioEvents[event.name].push event
    this



  ###
  # .ioUnbind(event, [callback])
  Unbind model triggers and stop listening for server events for a specific
  event and optional callback.

  The socket.io socket must either exist at `window.socket`, `Backbone.socket`,
  or `this.socket` or it must be passed as the second argument.

  @name ioUnbind
  @param {String} eventName
  @param {Object} io from active socket.io connection
  @param {Function} callback (optional) If not provided will remove all
  callbacks for eventname.
  @api public
  ###

  IOModel::ioUnbind = (eventName, io, callback) ->
    ioEvents = @_ioEvents or (@_ioEvents = {})
    globalName = @url() + ":" + eventName
    if "function" is typeof io
      callback = io
      io = @socket or window.socket or Backbone.socket
    events = ioEvents[eventName]
    unless _.isEmpty(events)
      if callback and "function" is typeof callback
        i = 0
        l = events.length

        while i < l
          if callback is events[i].cbLocal
            @unbind events[i].name, events[i].cbLocal
            io.removeListener events[i].global, events[i].cbGlobal
            events[i] = false
          i++
        events = _.compact(events)
      else
        @unbind eventName
        io.removeAllListeners globalName
      delete ioEvents[eventName]  if events.length is 0
    this


  ###
  # .ioUnbindAll()

  Unbind all callbacks and server listening events for the given model.

  The socket.io socket must either exist at `window.socket`, `Backbone.socket`,
  or `this.socket` or it must be passed as the only argument.

  @name ioUnbindAll
  @param {Object} io from active socket.io connection
  @api public
  ###
  IOModel::ioUnbindAll = (io) ->
    ioEvents = @_ioEvents or (@_ioEvents = {})
    io = @socket or window.socket or Backbone.socket  unless io
    for ev of ioEvents
      @ioUnbind ev, io
    this

  return IOModel
