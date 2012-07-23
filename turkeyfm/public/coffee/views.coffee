# load the namespace
App = window.App

TMPLID_PREFIX = 'template-'
compile_template = (template_name)->
  Handlebars.compile $("#"+ TMPLID_PREFIX + @template_name).html()

# Base View for all bubbler app views
class View extends Backbone.View
  initialize: ->
    if @template instanceof String
      @template = compile_template @template

  render: ->
    this.model? and @$el.html @template(this.model)
    this.collection? and @$el.html @template(this.collection)

# Views for all other views
class App.vApp extends View

  initialize: ->
    super.initialize()

class App.vBoard extends View
  initialize: ->
