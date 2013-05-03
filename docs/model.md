# Data-structure doc

1. room related

Common-Datastructure
    user: extends(common_userinfo, {
      room: Room.id,
      is_playing: whether the user is load audio and playing the song -- value:[1, 0]
    })

    room {
      admin: <uid>,
      users: [uid1, uid2, ...]
      current_song: {<dict>song_info}
      playlist: [sid1, sid2, ...] // playlist in room
      history: [sid: 'skip', sid: 'hearted'] 1386894:s|444482:p|460268:s|48180:s|1027376:s|188257:s
      available_channels: [red_heart, personal, ...]
    }

    song {
      creater: <uid>// user who choose the song
    }


### Only stored in client ###
    channel, and etc.
    user-playlist , []

    player-history, [{song: action}, ], maxium song: 20


