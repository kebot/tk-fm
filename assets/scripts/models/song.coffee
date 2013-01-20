define ['model'], (Model)->
  class Song extends Model
    url: "/song/#{@id}"


