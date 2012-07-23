# Backbone.sync
window.faker =
  board: [
      id: 123456
      title: '那些年我们追过的小清新'
      description: '那些年我们追过的小清新们'
      user_id: 241512
      create_time: 0 # what's the time format?
      bubs: []
      thumbnail: 'http://img3.douban.com/lpic/s9102157.jpg'
    ,
      title: 'BigBang !'
      thumbnail: 'http://img1.douban.com/lpic/s6944541.jpg'
    ,
      title: '妹妹坐船头'
      thumbnail: 'http://img1.douban.com/lpic/s7021742.jpg'
    ,
      title: '不万能的青年旅店'
      thumbnail: 'http://img5.douban.com/lpic/s4614409.jpg'
    ,
      title: '最炫民族风'
      thumbnail: 'http://img3.douban.com/lpic/s3814887.jpg'
    ,
      title: 'Nothing is True, Everything is premited!'
      thumbnail: 'http://img3.douban.com/lpic/s4052236.jpg'
    ,
      title: 'Code Playing !'
      thumbnail: 'http://img1.douban.com/lpic/s6944541.jpg'
    ,
      title: '飞机飞过天空'
      thumbnail: 'http://img1.douban.com/lpic/s6950503.jpg'
    ]

Backbone.sync = (method, model, options)->
  # /j/board/:boardid , delete, update, read
  # create /j/board


