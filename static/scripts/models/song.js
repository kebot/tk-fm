(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['models/io'], function(IOModel) {
    var Song;
    return Song = (function(_super) {

      __extends(Song, _super);

      function Song() {
        return Song.__super__.constructor.apply(this, arguments);
      }

      Song.prototype.idAttribute = 'sid';

      Song.prototype.url = "/song/" + Song.id;

      return Song;

    })(IOModel);
  });

}).call(this);
