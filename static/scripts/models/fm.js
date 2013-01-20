(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['backbone'], function() {
    var RadioSong;
    return RadioSong = (function(_super) {

      __extends(RadioSong, _super);

      function RadioSong() {
        return RadioSong.__super__.constructor.apply(this, arguments);
      }

      return RadioSong;

    })(Backbone.Model);
  });

}).call(this);
