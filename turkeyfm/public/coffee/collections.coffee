App = window.App

# url.root

class Collection extends Backbone.Collection
  urlRoot: '/j'


class App.cBubblers extends Collection
  url: ->
    if this.model.get('sid', false)
      return "/song/#{this.model.get('sid')}/bubblers"
    else if this.model.get('uid', false)
      return "/people/#{this.model.get('uid')}/bubblers"


