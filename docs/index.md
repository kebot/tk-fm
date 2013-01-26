Workflow for sync player position between players.

```
  ROOM {
    [current_song]
    [play list], { songinfo + creater }
  }
```
  1. `hearlisten` create a room.
  2. `hearlisten` choose his `personal channel` and get a playlist,
     defaultly, it will be stored in server-side.
                              repeat update_playerposition(creater will do this)
  3. `c` join the room, 



the play list will be stored in room.

// client.on_song_ends


