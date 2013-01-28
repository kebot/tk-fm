define [
  'models/io'
], (IOModel)->

  class Song extends IOModel
    idAttribute: 'sid'
    url: "/song/#{@id}"

