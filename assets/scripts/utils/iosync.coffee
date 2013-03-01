define ['utils/io'], (io)->
  #!
  # * backbone.iobind - Backbone.sync replacement
  # * Copyright(c) 2011 Jake Luer <jake@alogicalparadox.com>
  # * MIT Licensed
  #

  ###
  # Backbone.sync

  Replaces default Backbone.sync function with socket.io transport

  --- Assumptions

  Currently expects active socket to be located at `window.socket`,
  `Backbone.socket` or the sync'ed model own socket.
  See inline comments if you want to change it.
  --- Server Side

  socket.on('todos:create', function (data, fn) {
  ...
  fn(null, todo);
  });
  socket.on('todos:read', ... );
  socket.on('todos:update', ... );
  socket.on('todos:delete', ... );

  @name sync
  ###
  sync = (method, model, options) ->
    getUrl = (object) ->
      if options and options.url
        return if _.isFunction(options.url) then options.url() else options.url
      return null  unless object and object.url
      (if _.isFunction(object.url) then object.url() else object.url)

    cmd = getUrl(model).split("/")
    namespace = (if (cmd[0] isnt "") then cmd[0] else cmd[1])
    # if leading slash, ignore
    params = _.extend(
      req: namespace + ":" + method
    , options)

    params.data = model.toJSON() or {} if not params.data and model

    params.data = {
      method: method
      data:   params.data
    }

    # If your socket.io connection exists on a different var, change here:
    #io.emit namespace + ":" + method, params.data, (err, data) ->
    io.emit namespace, params.data, (err, data) ->
      if err
        options.error? err
      else
        options.success model, data, {}

