###
a simple amd-style `nunjuck` runtime
###

define 'nunjucks', ->
  class Environment
    constructor: ()-> console.log 'hello world'

    registerPrecompiled: (templates)->
      for name in templates
        @cache[name] = new Template

  env = new Environment()
  tmpl = env.getTemplate('test.html')

  require('test.html')

error = 'just an error'
not_print error

