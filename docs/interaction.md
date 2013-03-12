# Interaction

The interaction is important

Two kinds of interaction here.


After user interaction with the app.

[skip, heart, trash]

  FMClient ->
    skip, trash: re-request the playlist

  Server:
    then -)

    receive `skip` or `trash` action
    wait for `10(will be defined)` seconds, if
    vote ->
      sid: <song_id>
      action: <skip or 
      trigger: {
        'user_id': ...
        'device_id': ...
        other_user_info
      }
      voters: {
        [
          uid: <uid>
          action: 1
        ]
      }
      successed: 0

  Example Info:
    '<username> 想要切歌, 10人投票, 其中4人同意, 6人反对.'
    -- '10秒后切歌'

  --> server trigger 'next_song'


