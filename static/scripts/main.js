(function() {
  var bowerDefine, __isArray, __toString;

  require.config({
    baseUrl: '/static/',
    distUrl: '/static/dist'
  });

  __toString = Object.prototype.toString;

  __isArray = Array.isArray || function(obj) {
    return __toString.call(obj) === '[object Array]';
  };

  bowerDefine = function(package_name, deps, main_js, non_amd_callback) {
    var script_path, src_name;
    if (non_amd_callback == null) {
      non_amd_callback = null;
    }
    if (!__isArray(deps)) {
      non_amd_callback = main_js;
      main_js = deps;
      deps = [];
    }
    script_path = "components/" + package_name + "/" + main_js;
    if (non_amd_callback) {
      src_name = "" + package_name + "-src";
      define(src_name, deps, script_path);
      return define(package_name, [src_name], non_amd_callback);
    } else {
      return define(package_name, deps, script_path);
    }
  };

  bowerDefine('jquery', 'jquery.js');

  bowerDefine('socket.io', 'dist/socket.io.js');

  bowerDefine('underscore', 'underscore.js', function() {
    return window._;
  });

  bowerDefine('backbone', 'backbone.js', function() {
    return window.Backbone;
  });

  bowerDefine('nunjucks', 'browser/nunjucks.js', function() {
    return window.nunjucks;
  });

  bowerDefine('soundmanager', 'script/soundmanager2.js', function() {
    return window.soundManager;
  });

  define('soundmanager-ready', ['finish', 'soundmanager'], function(finish, soundManager) {
    return soundManager.setup({
      url: '/static/components/soundmanager/swf/',
      useHTML5Audio: true,
      onready: function() {
        return finish(soundManager);
      },
      ontimeout: function() {
        return console.error('soundManager is not ready');
      }
    });
  });

  require(['socket.io'], function(io) {
    var socket;
    socket = io.connect('/room');
    socket.on('connect', function() {
      return console.info('io-connect');
    });
    socket.on('disconnect', function() {
      return console.info('io-disconnect');
    });
    return socket.on('current_song', function(msg) {
      console.info('change current_song to', msg);
      return current_song.set(msg);
    });
  });

  /*
  require [
    'soundmanager-ready'
  ], (soundManager)->
    # method one
    sound_biu = soundManager.createSound
      id: 'biu'
      url: 'http://bubbler.labs.douban.com/public/audio/biu3.mp3'
    sound_biu.play()
  */


}).call(this);
