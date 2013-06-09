define 'soundmanager-wrap', [
  'finish'
  'jquery'
  'views/player/template'
], (finish, $, render_iframe)->
  use = {}
  use.iframe = true

  if use.iframe
    # http://www.ijusha.com/referer-anti-hotlinking/
    window.__iframe_html_string = render_iframe host: location.host
    window.onSoundManagerReady = (sm)->
      console.log 'soundManger in iframe ready'
      finish sm
      window.onSoundMangerReady = null
      window.__iframe_html_string = null

    iframe = $ '''<iframe
      id="turkey-player"
      src="javascript: parent.__iframe_html_string;"
      frameBorder="0"
      width="100"
      height="100"></iframe>'''
    $('body').append iframe
    iframe_window = iframe.get(0).contentWindow

  else
    require ['soundmanger'], (soundManger)->
      console.info 'soundManger is not in iframe'
      finish soundManger


define [
  'finish'
  'soundmanager-wrap'
], (finish, soundManager)->
  soundManager.debugFlash = false
  # some setup for sound-manager2
  soundManager.setup
    allowScriptAccess: 'sameDomain'
    url: "http://#{location.host}/static/components/soundmanager/swf/soundmanager2_flash_xdomain/"
    useHTML5Audio: true
    preferFlash: false
    #SM2 is ready to play audio!
    onready: -> finish soundManager
    ontimeout: -> console.error 'soundManager is not ready'
    waitForWindowLoad: true
    debugMode: false

