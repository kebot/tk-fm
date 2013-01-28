(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

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

  define('turkeyfm', ['underscore', 'backbone', 'collections/channel', 'collections/current_playlist', 'models/current_song', 'models/current_user', 'templates/iframeplayer', 'utils/io'], function(_, Backbone, Channel, current_playlist, current_song, current_user, iframeplayer, io) {
    var TurkeyFM, channel;
    current_song.on('play', function() {
      return console.log('current song is playing');
    });
    channel = new Channel();
    return TurkeyFM = (function() {

      function TurkeyFM() {
        this.play = __bind(this.play, this);

        var _this = this;
        _.extend(this, Backbone.Events);
        this.listenTo(current_song, 'finish', this.nextSong);
        this.listenTo(current_playlist, 'reset', function() {
          if (_.isUndefined(current_song.id) && current_playlist.size() > 0) {
            return _this.nextSong();
          }
        });
      }

      TurkeyFM.prototype.nextSong = function() {
        current_song.set(current_playlist.shift().toJSON());
        return current_song.save();
      };

      TurkeyFM.prototype.initPlayer = function() {
        var iframe;
        window.AudioPlayer = iframeplayer({
          host: location.host
        });
        iframe = $('<iframe\nid="turkey-player"\nsrc="javascript: parent.AudioPlayer;"\nframeBorder="0"\nwidth="100"\nheight="100"></iframe>');
        $('body').append(iframe);
        this.iframewindow = iframe.get(0).contentWindow;
        return this.iframewindow.current_song = current_song;
      };

      TurkeyFM.prototype.play = function() {
        return this.iframewindow.player.play();
      };

      TurkeyFM.prototype.rock = function() {
        this.initPlayer();
        io.emit('join', 'default_room');
        return channel.fetch({
          success: function() {
            if (current_playlist.size() === 0) {
              return channel.each(function(model) {
                return current_playlist.create(model.toJSON());
              });
            }
          }
        });
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

  require(['turkeyfm', 'jquery'], function(FM, $) {
    var lets;
    lets = new FM();
    lets.rock();
    return $("button").click(function() {
      return lets.play();
    });
  });

}).call(this);
