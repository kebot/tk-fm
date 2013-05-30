define [
  'underscore'
  'jquery'
  'backbone'
], (_, $, Backbone)->

  parse = (text)->
    #return _.flatten(_.map(
    return _.chain(text.split('\n')).map(splitline = (line, index)->
      if _.isNumber(index)
        times = []
      else if _.isArray index
        times = index
      else
        console.error 'wrong index param'

      if line.length >= 10 and line[0] is '[' and line[3] is ':' and line[6] is '.' \
                          and line[9] is ']'
        times.push ((parseInt(line.slice(1, 3)) * 60 + 
          parseInt(line.slice(4, 6))
        ) * 100 + parseInt(line.slice(7, 9))) * 10
        return splitline(line.slice(10), times)
      else
        return _.map times, (t)-> {
          'text': line,
          'time': t
        }
    ).flatten().sortBy((item)->
      return item['time']
    ).value()

  class LyricController extends Backbone.View
    initialize: ->

    render: ->
      @stopListening()
      if not @model.id
        return

      $.getJSON "http://l:5000/j/song/#{@model.id}/lyric", (response)=>
        if response.r != 0
          return

        @lyrics = parse(response.lyric)
        _last_index = false

        @listenTo @model, 'change:position',  ->
          index = @findIndex(@model.get('position'))

          if index < 0
            return

          if _last_index == index
            return
          else
            @$el.html @lyrics[index].text

    findIndex: (now, begin=0)->
      if @lyrics.length == 0
        return -1

      _i = begin
      while true
        # already the last one
        if _i == @lyrics.length - 1
          return _i

        item = @lyrics[_i]
        next = @lyrics[_i+1]

        if _i == 0 and now < item.time
          # less then the first one
          return _i

        if item.time < now < next.time
          return _i

        if now > next.time
          _i = _i + 1
          continue

        if now < item.time
          _i = _i - 1
          continue

        console.error('_i something unexcepted')
        break

