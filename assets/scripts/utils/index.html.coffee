define 'index.html', ['nunjucks'], (nunjucks)->
  templates = {}
  templates["index.html"] = (->
    root = (env, context, frame, runtime)->
      output = ""
      output += "\n\n\n"
      output
    {root: root}
  )()
  nunjucks.env = new nunjucks.Environment([])
  nunjucks.registerPrecompiled templates

