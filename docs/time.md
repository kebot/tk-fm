# all time in this project are stored in utc timestamp(milliseconds)

```
require ['moment'], (moment)->
  position = moment(
    model.get('started_at')
  ).from_now()

  moment.duration(
    model.get('position')
  )
```



