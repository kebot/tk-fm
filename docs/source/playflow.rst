Every client has one queuelist~(device id)

Only two operation is available here:

Operations to songlist:
------------------------

1. add song to queue
2. delete song in queue(can only delete song added by yourself)

(client) current_song is not set
-> finish(sid=None)
(server) choose one song
<- set current_song
<- <songlist> delete first song
(client) playing the song, report the playerposition

(client)current_song finish playing
-> finish(sid=<sid>)

(client) playlist is empty
-> auto add song to playlist

.. codeblock python

>>> print userlist
(1, kebot, iPad), (2, kebot, MacBook), (3, kebot, vivo),
(4, queenie, PC), (5, who, weixin)

>>> print currentsong
{
  'sid': 0,
  'creater': 0,
}

>>> print songlist
[
  (song1, kebot),
  (song2, who),
  (song3, queenie),
  (song4, kebot)
]

on_playing -> report begin

get player status for every device

method: <patch:current_song>

the first reporter will be baseline.

[1, 'playing', <report_time>]
[2, 'pausing', <report_time>]

If half(a variable) of the client is report finish, the nextsong will be played!



