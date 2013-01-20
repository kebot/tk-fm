(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['jquery', 'backbone', 'kendo-core'], function($, Backbone) {
    var KendoCalendar;
    return KendoCalendar = (function(_super) {

      __extends(KendoCalendar, _super);

      function KendoCalendar() {
        return KendoCalendar.__super__.constructor.apply(this, arguments);
      }

      KendoCalendar.prototype.initialize = function(options) {
        KendoCalendar.__super__.initialize.call(this, options);
        this.$el.kendoCalendar(options);
        return this.calendar = $el.data('kendoCalendar');
      };

      return KendoCalendar;

    })(Backbone.View);
  });

}).call(this);
