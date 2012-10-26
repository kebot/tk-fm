#! Keith Yao

# Give backbone a namespace: App
App = {}

jQuery ->
  app_router = new window.App.AppRouter()
  Backbone.history.start()

window.App = App
