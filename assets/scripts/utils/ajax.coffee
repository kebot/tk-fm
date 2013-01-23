define ['jquery', 'underscore'], (
  $, _
)->
  # require ['utils/ajax'], (ajax)-> ajax.json
  json: (url, method, data, callback)->
    if _.isFunction method
      callback = method
      method = 'get'
      data = null

    $.ajax
      url: url
      type: method.toUpperCase()
      data: JSON.stringify(data) if data
      dataType: 'json'
      contentType: 'application/json'
      processData: false
      success: callback

