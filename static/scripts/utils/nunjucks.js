
/*
a simple amd-style `nunjuck` runtime
*/


(function() {
  var error;

  define('nunjucks', function() {
    var Environment, env, tmpl;
    Environment = (function() {

      function Environment() {
        console.log('hello world');
      }

      Environment.prototype.registerPrecompiled = function(templates) {
        var name, _i, _len, _results;
        _results = [];
        for (_i = 0, _len = templates.length; _i < _len; _i++) {
          name = templates[_i];
          _results.push(this.cache[name] = new Template);
        }
        return _results;
      };

      return Environment;

    })();
    env = new Environment();
    tmpl = env.getTemplate('test.html');
    return require('test.html');
  });

  error = 'just an error';

  not_print(error);

}).call(this);
