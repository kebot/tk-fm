# https://code.google.com/p/drhac/wiki/Protocol

type*:
  b: ban
  e: end
  n: new
  p: played
  s: skip
  u: unrate
  r: rate
uid: current_user_id
r: random number[will be generated in python side]
h: history <sid>:</[psbr]/>|...
sid: <Song ID>
aid: <Album ID>
rest: <sid>|<sid2>...
status: p -> playing
du: // not require

----------------------------------------------------

User Action:
  Rate, Trash, Unrate, Skip
  if history.count()
    {h: history.__str__()}


finish playing:
  history.add current_song
  -> io -> finish: {sid: <current_sid>}

  if channel.count() == 0
    moreSong, request more song with history


