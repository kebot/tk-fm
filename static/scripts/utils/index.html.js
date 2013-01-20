(function() {

  define('index.html', ['nunjucks'], function(nunjucks) {
    var templates;
    templates = {};
    templates["index.html"] = (function() {
      var root;
      root = function(env, context, frame, runtime) {
        var output;
        output = "";
        output += "\n\n\n";
        return output;
      };
      return {
        root: root
      };
    })();
    nunjucks.env = new nunjucks.Environment([]);
    return nunjucks.registerPrecompiled(templates);
  });

}).call(this);
