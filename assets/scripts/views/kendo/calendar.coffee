define ['jquery', 'backbone', 'kendo-core'], ($, Backbone)->

  class KendoCalendar extends Backbone.View

    initialize: (options)->
      super options
      this.$el.kendoCalendar options
      @calendar = $el.data('kendoCalendar')


