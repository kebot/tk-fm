(function() {
  var bowerDefine, __isArray, __toString;

  require.config({
    baseUrl: '/static/scripts/',
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
    script_path = "http://localhost:5000/static/components/" + package_name + "/" + main_js;
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

  bowerDefine('backbone', ['jquery', 'underscore'], 'backbone.js', function() {
    return window.Backbone;
  });

  bowerDefine('handlebars', 'handlebars.runtime.js', function() {
    return window.Handlebars;
  });

  bowerDefine('nunjucks', 'browser/nunjucks.js', function() {
    return window.nunjucks;
  });

  bowerDefine('soundmanager', 'script/soundmanager2.js', function() {
    return window.soundManager;
  });

  /*
  define 'soundmanager-ready', [
    'finish',
    'soundmanager'
  ], (finish, soundManager)->
    # some setup for sound-manager2
    soundManager.setup
      url: '/static/components/soundmanager/swf/'
      useHTML5Audio: true
      #SM2 is ready to play audio!
      onready: -> finish soundManager
      ontimeout: -> console.error 'soundManager is not ready'
  
  
  require [
    'socket.io'
  ], (io)->
    socket = io.connect '/room'
    socket.on 'connect', -> console.info 'io-connect'
    socket.on 'disconnect', -> console.info 'io-disconnect'
    # custom events, current_song changed
  
    socket.on 'current_song', (msg)->
      console.info 'change current_song to', msg
      #current_song.set msg
  
    room_name = 'room1'
    socket.emit 'join', room_name
  */


  require(['jquery', 'backbone', 'utils/ajax', 'models/current_user'], function($, Backbone, ajax, current_user) {
    return ajax.json('/account', function(r) {
      if (r.r === 0) {
        return current_user.set(r.user_info);
      } else {
        return require(['views/mod/login'], function(mod_login) {
          $('body').append(mod_login.el);
          return mod_login.show();
        });
      }
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
