(function() {

  define('template', [], function() {
    var View;
    return View = (function() {

      function View() {}

      View.prototype.el = $('body');

      View.prototype.template = 'body';

      View.prototype.render = function() {
        return $('.container').render();
      };

      return View;

    })();
  });

}).call(this);
