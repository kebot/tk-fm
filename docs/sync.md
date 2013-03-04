Sync `playerposition`(`current_song`) and `songlist` between users
----------------------------------------------------------------------------

Python Side:
`time.time() * 1000`

1. is this a unix timestamp
2. is this a utc time

> @TODO programing process time to access more currently time.

# Sync time **Stable**
=========================================
Device-time could be different, so 

  1. Make a request from current device to get the time from target device
  2. Calculate time spent on roundtrip
  3. Time difference is: (TargetDeviceTime - TimeSpentOnRoundTrip) - CurrentDeviceTime

[Time Sync Algorithm](http://www.cnblogs.com/lbq1221119/archive/2010/01/14/1647829.html)

dj -> {report_time: ts, position: ta} -> broadcast ===> 
    listener:
      seekTo-> current_time - report_time + position

who report the player position. **trash**
-----------------------------------------
only *dj* for the song can report player-position, but not everyone is
playing, someone is just listening(no player loaded, so he can not
report the current player position).

# Sync current_song, process user actions:

dj.on 'finish', -> 
  current_song
  nextsong = playerlist.shift()

  player_history.append current_song
  current_song.set next_song.toJSON()

## User actions ##

User can trigger actions for the `current_song`
  trash, heart: only login user

  skip: <by vote>, agree or reject
    5 players: tom , lee, keith, hellen, queenie
      tom ask to skip the song, 1/1
      lee agree - 2/2
      keith reject - 2/3
      hellen rejct - 2/4
      queenie say nothing

    then the song will be skipped


# Sync play-list #
there is three kinds of actions for `playlist`

**remove** (sid)
  user:  can only remove song created by himself

**add(sid)**
  unlimited

** sort(sid, weight) **

sort the songlist by change the weight of collection song
```coffeescript
    comparator: -> 
      @get('weight') // default is current_time

```
-----------------------------------------------------------------------------
# the admin of the room **Trash**

  the admin is always load a player, report the player position,
switch songs.
  if admin leave the room, must choose another admin


if current_song.dj not in room.userlist
    current_song.set('dj': room.admin)

-----------------------------------------------------------------------------

machine action:

if the playlist is empty, what will happen?

-------------------------------------------

  there is two kinds of choosen song in player list, 
    1. user selected song
    2. machine selected song

    the user selected song will always in the front of the playlist.

  if the current_playlist is empty, every user will request songs from
rooms available channel.
  when the room's playerlist is empty, every user pop the first song to
the room's playlist.

  user actions will be use for update the playerlist.



