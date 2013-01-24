
/*
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


(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define('collections/channel', ['backbone', 'models/song'], function(Backbone, Song) {
    /*
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
    */

    var ChannelListCollection;
    return ChannelListCollection = (function(_super) {

      __extends(ChannelListCollection, _super);

      function ChannelListCollection() {
        return ChannelListCollection.__super__.constructor.apply(this, arguments);
      }

      ChannelListCollection.prototype.model = Song;

      ChannelListCollection.prototype.url = function() {
        return '/fm/mine/playlist';
      };

      ChannelListCollection.prototype.parse = function(response) {
        if (response.r === 0) {
          return response.song;
        }
      };

      return ChannelListCollection;

    })(Backbone.Collection);
  });

  define('turkeyfm', ['underscore', 'backbone', 'collections/channel', 'models/current_song', 'models/current_user', 'templates/iframeplayer'], function(_, Backbone, Channel, current_song, current_user, iframeplayer) {
    var TurkeyFM, channel;
    channel = new Channel();
    return TurkeyFM = (function() {

      function TurkeyFM() {
        _.extend(this, Backbone.Events);
        this.listenTo(channel, 'sync', this.synced);
      }

      TurkeyFM.prototype.synced = function() {
        return current_song.set(channel.shift().toJSON());
      };

      TurkeyFM.prototype.initPlayer = function() {
        window.AudioPlayer = iframeplayer({
          host: location.host
        });
        return $('body').append('<iframe\nsrc="javascript: parent.AudioPlayer;"\nframeBorder="0"\nwidth="0"\nheight="0"></iframe>');
      };

      TurkeyFM.prototype.rock = function() {
        this.initPlayer();
        return channel.fetch();
      };

      return TurkeyFM;

    })();
  });

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

  require(['turkeyfm'], function(FM) {
    var lets;
    lets = new FM();
    return lets.rock();
  });

}).call(this);
