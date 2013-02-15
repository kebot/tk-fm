User -> Device

Users may login from diffient device at same time, so we need to store a
unique id to recognise every different device.

  <uid 227541>, <device-id 'macbook'>

  <uid 227541>, <player device>

  song: {
    creater: <int:uid>,
    // but who to play the song.
  }

Play control flow:
-> Creater's Playing Device. (One player can only have one playing device.)
-> Creater not online or Creater has no playing device.
-> Others play the song. If no one play, the song will be skipped. ( or
room master will play )

One play, others follow!
