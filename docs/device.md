User -> Device

Three kinds of `id` for every connected device
  <web-session id> - Stored in Cookies, unique for every device.
  These id is related to web-session:
    - <Douban uid>
    - <Device id>

  <SocketIo Session Id> - Unique for every connection.(One device may have many
connection, but only one in the same time)

Device id
----------------------------------------------------------------------------
Users may login from diffient device at same time, so we need to store a
unique id to recognise every different device.
Case session-id is secret for every user, so it can not be use as a
unique id.

  relate key:
    key: <uuid>, 
    value: <session-id>

  <uid 227541>, <device-id 'macbook'>
  <uid 227541>, <player device>

  song: {
    creater: <int:uuid>,
    // but who to play the song.
  }

-----------------------------------------------------------------------------
Play control flow:
-> Creater's Playing Device. (One player can only have one playing device.)
-> Creater not online or Creater has no playing device.
-> Others play the song. If no one play, the song will be skipped. ( or
room master will play )

One play, others follow!
