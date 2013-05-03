=========================
Events doc in turkeyfm
=========================

There are three kinds of event in this project.

1. Server-side events
2. Client-Server events
3. Client-Side events

for example, if one user want to modify the player-position of the
current_song.


methods
-------------------------

for better understand, methods are all http method in messages.

Get, Post, Put, Delete and Patch


models
------------------------
Socket.io

Client-Server ..

  channel: 'current_song'
  {
    method: 'patch',
    data: {
      'player-position': 111
    },
  }

when the server receives the message, it will post to redis.

redis-channel: 'room-<roomid>-current_song'

  {
    method: 'patch',
    data: {
      'player-position': 111
    },
    except: ['client-id']
  }

* method is http-method: 'GET', 'POST', 'PATCH', 'DELETE'
client receive this message, and update the data.

* it will works well with model, but when it comes to collection.

Work with collection
--------------------------------

Modify one model in collection, 

channel: 'current_playlist'
get, patch, delete

  {
    _id: underscore field <model_id>
    method...
    data: {}
  }

post(no hidden field):

  {
    method: 'post',
    data: {
    }
  }


How to reorder model in collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

there is a `composer` element, just have two patch
{
  _id: 123456
  method: 'patch'
  data: {
    order: xxx
  }

}




