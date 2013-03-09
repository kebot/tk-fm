if typeof window._rock_host == 'undefined'
  window._rock_host = location.host

require.config
  baseUrl: "http://#{window._rock_host}/static/scripts/"
  distUrl: "http://#{window._rock_host}/static/dist"

__toString = Object.prototype.toString
__isArray = Array.isArray or (obj)-> __toString.call(obj) == '[object Array]'

bowerDefine = (package_name, deps, main_js, non_amd_callback=null)->
  if not __isArray deps
    non_amd_callback = main_js
    main_js = deps
    deps = []

  script_path = "http://#{window._rock_host}/static/components/#{package_name}/#{main_js}"
  if non_amd_callback
    # define for non amd package
    src_name = "#{package_name}-src"
    # console.debug src_name, deps, script_path
    define src_name, deps, script_path
    define package_name, [src_name], non_amd_callback
  else
    # define for amd package
    define package_name, deps, script_path

bowerDefine 'jquery', 'jquery.js'
bowerDefine 'socket.io', 'dist/socket.io.js'
bowerDefine 'moment', 'moment.js'
bowerDefine 'underscore', 'underscore.js', -> window._
bowerDefine 'backbone', ['jquery', 'underscore'], 'backbone.js', -> window.Backbone
bowerDefine 'handlebars', 'handlebars.runtime.js', -> window.Handlebars
bowerDefine 'nunjucks', 'browser/nunjucks.js', -> window.nunjucks
bowerDefine 'soundmanager', 'script/soundmanager2.js', -> window.soundManager

#bowerDefine 'gsap-timelinelite', 'src/uncompressed/TimeLineLite.js'
#bowerDefine 'gsap-timelinemax', 'src/uncompressed/TimeLineMax.js'
#bowerDefine 'gsap-tweenlite', 'src/uncompressed/TweenLite.js'
#bowerDefine 'gsap-tweenmax', 'src/uncompressed/TweenMax.js'
bowerDefine 'tweenMax', 'src/uncompressed/TweenMax.js'
# plugins available: cssplugin, cssruleplugin, scrolltoplugin, etc...

bowerDefine 'iobind', 'dist/backbone.iobind.js', -> window.soundManager
bowerDefine 'iosync', 'dist/backbone.iosync.js', -> window.soundManager

# redirect libs
define 'utils/io-init', 'utils/io.js'
#define 'soundmanager-ready', 'views/player.js'
define 'use', 'utils/use.js'
# // finish define libs

