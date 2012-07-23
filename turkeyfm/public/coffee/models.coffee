App = window.App

# url.root

class Model extends Backbone.Model
  urlRoot: '/j'

  # Default parser for BubblerModel
  parse: (response) ->
    if response.error
      return false
    else
      this.set response
 

class App.mUser extends Model
  url: '/people/' + this.id

  defaults: {
    'uid': 'hearlisten'
    'title': '已注销'
    'icon': 'http://img3.douban.com/icon/user_normal.jpg'
    'homepage': 'http://www.douban.com/people/hearlisten'
  }

class App.mSong extends Model
  url: '/song/' + this.id

  defaults: {
    'sid': 1
    'song_name': 'Untitled'
    'artist': 'UnknowArtist'
    'album': 'UnknowAlbum'
    'cover': 'http://img3.douban.com/pics/music/default_cover/mpic/music-default.gif'
  }

class App.mBubbler extends Model
  url: '/bubbler/' + this.id

  toggleRate: ->
    # send PUT http request.
    this.save({rate: ! this.get('rate')})

  interest: ->
    # Toggle Interest
    this.save({interest: ! this.get('interest')})

  defaults: {
    'rate'
  }


class App.mBoard extends Model
  url: '/board/' + this.id
