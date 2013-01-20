(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['backbone'], function(Backbone) {
    var AppRouter;
    return new (AppRouter = (function(_super) {

      __extends(AppRouter, _super);

      AppRouter.prototype.routes = {
        '/song/:sid': 'change_song',
        '/place/:name': 'switch_to_place'
      };

      function AppRouter(options) {
        this.options = options;
      }

      AppRouter.prototype.run = function() {
        var result;
        result = Backbone.history.start({
          pushState: true
        });
        if (result === true) {
          return console.log('successfully running the application!');
        }
      };

      AppRouter.prototype.registerApplication = function(app) {};

      return AppRouter;

    })(Backbone.Router));
  });

}).call(this);
