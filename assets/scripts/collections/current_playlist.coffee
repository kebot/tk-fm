define [
  'collections/io',
  'models/song',
  'io'
], (IOCollection, Song)->

  class Playlist extends IOCollection
    model: Song


