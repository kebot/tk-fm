====================================
The Review of Relevant Literature
====================================

Background Information
====================================

Pandora and Music DNA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pandora is an automated music recommendation service.
The service plays musical selections of a certain genre based on the user's artist selection.
The user then provides positive or negative feedback for songs chosen by the service, which
are taken into account when Pandora selects future songs.

Pandora (pandora.com) has more than 750000 songs, this figure far behind MOG, Napster or
RDIO music service. But each song Pandora by the review team members of the audit,
then according to the nearly 400 music attribute is added to the "Music Genome Project"
(Music Genome Project) project.

Westergren said, the music genome project provides a "music DNA", but the Pandora website
is based on this, try to determine the songs for you to play the next song according to
your taste. On the Pandora website, the user can through the "top", "step on" feedback
to the influence of it to play songs.

Westergren: "as time goes by, we will find out you 'top' and 'on' mode. Pandora trying
to be like to know what you like, don't like what the record store clerk."

If you "on the" Jonny Mitchell (Joni Mitchell, female) of a song, this will not affect
your playlist male singer, but if you continue to "step on" female singer, the system
will pay attention to this mode, start reduced accordingly for you to play the song song.

Slacker Radio
~~~~~~~~~~~~~~~~~~~~~

Slacker Radio (slacker.com) using a different music recommendation, it currently
has about 3500000 songs. Jonathan Sasse vice president Slacker Radio said the
service marketing, the biggest feature is its "manual arrangement" genres of music
channel. These channels by a person with "rich experience for the radio program".

Sasse said: "the DJ specific control the song playing, because of the interaction
between community and the radio, we can observe the people's acceptance of these
songs, songs received more or bad comments, and these factors will affect the
operation of DJ.

Recommendation algorithms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recommender systems or recommendation systems are a subclass of information
filtering system that seek to predict the 'rating' or 'preference' that user
would give to an item (such as music, books, or movies) or social element (e.g.
people or groups) they had not yet considered, using a model built from the
characteristics of an item (content-based approaches) or the user's social
environment (collaborative filtering approaches). [1]_

1. Content based recommendation
  Content-based recommendation is the continuation
  and development of information filtering technology, it is recommended in the
  project and make the content information, without the need for user evaluation
  according to the project, get the user interest information method more need to
  use machine learning are described from the features of the contents of the case.
  Depending on the data model of user learning methods in use, are commonly used in
  neural network decision tree, and based on the vector representation. Content of
  the user data is based on historical data are required to have the user, user data
  model with user preferences change.

2. Collaborative filtering recommendation
   Collaborative filtering recommendation technology is the recommendation system
   in the application of the earliest and one of the most successful technology.
   It usually adopts the nearest neighbor technique, using the user's historical
   preferences information to calculate the distance between users, weighted
   evaluation and then use the nearest neighbors of target user user of the product
   evaluation value to predict the extent of the target user preferences for specific
   commodities, the system according to the preference of the target user to recommend.
   Collaborative filtering is the biggest advantage is that no special requirements on
   the recommendation of object, be able to handle unstructured complex objects, such
   as music, movie.

3. Association Rules Recommendation Based on association rules based on the purchase
   of goods, as a rule, the rules for recommendation object. Association rules mining
   can find correlations between different products in the sales process, it has been
   successfully applied in the retail industry. Management rule is the statistics in
   a transaction database to buy what proportion of goods set X the transaction also
   bought goods set Y, its intuitive meaning is that users have much inclined to buy
   other goods when buying some goods. For example, at the same time the milk purchase
   many people will buy bread at the same time.

4. The utility based on the recommendation of calculation based on utility is used on
   the project to the user, the core problem is how to each user to create a utility
   function, therefore, the user data model is largely adopted by the utility function
   of decision system. Based on the utility recommended benefit is that it can not
   product attributes, such as the provider's reliability and product availability,
   taking into account the utility computing.

5. The recommended methods have advantages and disadvantages, so in practice,
   combination recommendation (Hybrid Recommendation) are often used. Research and
   application of the most is the content recommendation and collaborative filtering
   recommendation of the combination. The simplest approach is respectively with
   content-based approach and collaborative filtering recommendation approach to
   generate a recommended the prediction results, and then use a method combining
   the results. Although in theory there are many kinds of recommendation combination
   method, but not necessarily in a specific problem are valid, combination recommendation
   is one of the most important principle is to avoid or compensate for their recommendation
   technology through the combination of weakness.

.. [1] ^ a b Francesco Ricci and Lior Rokach and Bracha Shapira, Introduction to Recommender Systems Handbook, Recommender Systems Handbook, Springer, 2011, pp. 1-35
.. [2] http://en.wikipedia.org/wiki/Recommender_system

Live time music service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project is web based live time service, there have some live time web service in
the real internet. They are basicly rely on server side push technology.

Turntable [4]_ is the first web service have the same idea with me, it is based on
web. It let you to listening to music with your friends. Listen to music selected by
people, not the algorithms above.

It let player listening to music selected by the user, I have the same idea with turntable.
But if no one is select song, the music will be stopped, so I will write some algorithm
to recommend song to the user in one room.

It's idea also copy to China by Xiami's loop.[5]_


.. [3] http://en.wikipedia.org/wiki/Long_polling#Long_polling
.. [4] https://turntable.fm/about
.. [5] http://loop.xiami.com

Text
====================================

The exsiting project related to my idea
---------------------------------------

Github has released a project called play that used in their office, it is totally opensource
and it write in ruby. Play is good enough, but it is not a offical product, it use iTunes to
play music, but not everyone use it. [1]_

In this project:

Native clients use Pusher to be updated in realtime. They will show what is currently playing,
and with some clients, what is queued. All clients are built to consume the Shoutcast stream.

And the server is write in Ruby and AppleScript(to control iTunes).

Like many people have experienced on iOS with apps that use your music library, iTunes Match
royally screws this up. iTunes does nothing to differentiate songs that are actually available
on disk, and those that would need to be pulled down first by Match in order to play them.
This screws up Play, just as it screws up iOS apps that naively (not their fault) attempt to
play something out of the music library that is actually only available via Match.
This can hopefully be addressed in the future. For now, skip Match.

iTunes march is one of the good music recommend service. Here I will use doubanfm to recommend
songs.

.. [1] https://github.com/play/play

Online-music services
-------------------------

Music services in China
~~~~~~~~~~~~~~~~~~~~~~~~

2012, along with the increasing of intelligent mobile phone sales, mobile and
popularization of mobile network bandwidth terminal continues to improve, the
use of all kinds of mobile application store rate is also rising, mobile
Internet users continues to grow. Under its impetus, the steady growth of the
wireless music market scale. In 2012, the wireless music market size in China
reached 2720000000 yuan (content providers to total revenue growth of 13.3%),
more than 2400000000 yuan in 2011.

Wireless music user, intelligent mobile phone function of increasingly powerful
and price continues to decline, greatly reduces the threshold for the use of
intelligent mobile terminal, mobile Internet application innovation boom, the
rapid growth of mobile phone users scale to promote wireless music user growth.
By the end of 2012 users in China, the wireless music market size of close to
750000000, in a mobile subscriber penetration rate is 66.9%, after the instant
messaging, mobile phone search.

The momentum of development in 2012 of China's radio music the overall market
is good, the business model, as operators continue to the upstream and
downstream permeability, CP and SP integration, terminal manufacturers to
expand its market space unceasingly and wireless music user demand continues
to increase, the wireless music industry pattern is in constant collision
groping for the optimal model, and then drive the innovation application
increases ceaselessly, industry penetration gradually strengthen.


Big music service
~~~~~~~~~~~~~~~~~~~~~~~~

Rdio (online music service) (http://rdio.com/) is an amazing way to discover
new music. I realize I'm biased because I help design Rdio, but I genuinely
believe that we have built one of the best music discovery services on the planet.
Without Rdio, I would never have discovered dozens of albums that have become some
of my favorites of all time.

Pandora (http://pandora.com). Put in an artist or song that you do like, then thumb
up/down tracks so it learns what you like and don't. It doesn't take long to figure
you out and start suggesting things you've never heard but want to hear.

Spotify (http://www.spotify.com/). Similar to Pandora in many respects. I don't use
it much, but many of my friends love it.

SoundCloud (http://soundcloud.com/). I use this to follow independent musicians and
a few big-named artists. For the indies, this is sometimes their only output channel.
For the big-name acts, there are often extras and live tracks released via SoundCloud
that aren't available elsewhere.

Twitter (http:/twitter.com). Follow artists you admire. Then follow the artists they
follow and/or interact with (see Ethan Hein's answer re: Questlove).

Bandcamp (http://bandcamp.com/). Another great way to track indie artists. You can
browse by tag (read: genre) and artists can recommend other artists.


Development Tools
-----------------

The main language I use is CoffeeScript_ and Python_.

CoffeeScript
~~~~~~~~~~~~
CoffeeScript is a little language that compiles into JavaScript. Underneath that awkward
Java-esque patina, JavaScript has always had a gorgeous heart. CoffeeScript is an attempt
to expose the good parts of JavaScript in a simple way.

The golden rule of CoffeeScript is: "It's just JavaScript". The code compiles one-to-one
into the equivalent JS, and there is no interpretation at runtime. You can use any existing
JavaScript library seamlessly from CoffeeScript (and vice-versa). The compiled output is
readable and pretty-printed, passes through JavaScript Lint without warnings, will work in
every JavaScript runtime, and tends to run as fast or faster than the equivalent handwritten
JavaScript.

Backbone
~~~~~~~~~
The Backbone_ gives structure to web applications by providing models with key-value binding
and custom events, collections with a rich API of enumerable functions, views with declarative
event handling, and connects it all to your existing API over a RESTful JSON interface.

jQuery
~~~~~~
jQuery_ is a fast, small, and feature-rich JavaScript library. It makes things like HTML
document traversal and manipulation, event handling, animation, and Ajax much simpler with
an easy-to-use API that works across a multitude of browsers. With a combination of versatility
and extensibility, jQuery has changed the way that millions of people write JavaScript.

Handlebars
~~~~~~~~~~
Handlebars_ provides the power necessary to let you build semantic templates effectively with
no frustration. Mustache templates are compatible with Handlebars, so you can take a Mustache
template, import it into Handlebars, and start taking advantage of the extra Handlebars features.

Less
~~~~~
less.css_ is a dynamic stylesheet language. LESS extends CSS with dynamic behavior such as
variables, mixins, operations and functions. LESS runs on both the server-side (with Node.js and
Rhino) or client-side (modern browsers only).

With these pre-compile technology, I need something to auto compile files for me, I use grunt_
to build javascript tasks. It makes me much easiler to create task and run it.

SoundManager
~~~~~~~~~~~~
To play music in the browser, I use a lib named SoundManager_. SoundManager 2 makes it easier
to play audio using JavaScript.

Using HTML5 and Flash, SoundManager 2 provides reliable cross-platform audio under a single
JavaScript API. I can create cross-browser music player easiler with it.


Python is another beautiful language. The server side will be write in Python.

Flask
~~~~~~
Flask_ is a easy and beautiful web framework. Flask is a microframework for Python based on
Werkzeug, Jinja 2 and good intentions. And before you ask: It's BSD licensed!

Flask will be used to create the web server. User use this to decide where to join the room,
which music will be played and when to switch rooms.

To live connect to the server and client, websocket(socket.io) will be used to communicate
between server and client. Every single connection is based on a user's device.

gevent and Socket.io
~~~~~~~~~~~~~~~~~~~~~
Node.js provide the best solution of socket.io, python has it's own implementation called
gevent socket.io.

Gevent_ is a coroutine-based Python networking library that uses greenlet
to provide a high-level synchronous API on top of the libevent event loop.

Features include:

* Fast event loop based on libevent (epoll on Linux, kqueue on FreeBSD).
* Lightweight execution units based on greenlet.
* API that re-uses concepts from the Python standard library (for example there are Events and Queues).
* Cooperative sockets with SSL support »
* DNS queries performed through libevent-dns.
* Monkey patching utility to get 3rd party modules to become cooperative »
* Fast WSGI server based on libevent-http »

gevent is inspired by eventlet but features more consistent API, simpler implementation and
better performance. Read why others use gevent and check out the list of the open source
projects based on gevent.

Socket.IO is a WebSocket-like abstraction that enables real-time communication between a
browser and a server. gevent-socketio is a Python implementation of the protocol.

The reference server implementation of Socket.IO runs on Node.js and was developed by
LearnBoost. There are now server implementations in a variety of languages.

One aim of this project is to provide a single gevent-based API that works across the
different WSGI-based web frameworks out there (Pyramid, Pylons, Flask, web2py, Django,
etc...). Only ~3 lines of code are required to tie-in gevent-socketio in your framework.
Note: you need to use the gevent python WSGI server to use gevent-socketio.

So my python project is heavily rely on gevent as it's server and socket.io protocal.

Redis
~~~~~~~~~~~~~~

I have seriously consider whether I need to use MySQL or other relationship database.
But the answer is YES, but not now.

I use redis_ to store all my data and caches.

Redis is an open source, BSD licensed, advanced key-value store. It is often referred
to as a data structure server since keys can contain strings, hashes, lists, sets and
sorted sets.

You can run atomic operations on these types, like appending to a string; incrementing
the value in a hash; pushing to a list; computing set intersection, union and difference;
or getting the member with highest ranking in a sorted set.

In order to achieve its outstanding performance, Redis works with an in-memory dataset.
Depending on your use case, you can persist it either by dumping the dataset to disk every
once in a while, or by appending each command to a log.

Redis also supports trivial-to-setup master-slave replication, with very fast non-blocking
first synchronization, auto-reconnection on net split and so forth.

Other features include Transactions, Pub/Sub, Lua scripting, Keys with a limited time-to-live,
and configuration settings to make Redis behave like a cache.

You can use Redis from most programming languages out there.
Redis is written in ANSI C and works in most POSIX systems like Linux, *BSD, OS X without
external dependencies. Linux and OSX are the two operating systems where Redis is developed
and more tested, and we recommend using Linux for deploying. Redis may work in Solaris-derived
systems like SmartOS, but the support is best effort. There is no official support for Windows
builds, but Microsoft develops and maintains a Win32-64 experimental version of Redis.

Redis pubsub is another important technology I will use. With pubsub, I can SUBSCRIBE, UNSUBSCRIBE
and PUBLISH implement the Publish/Subscribe messaging paradigm where (citing Wikipedia) senders
(publishers) are not programmed to send their messages to specific receivers (subscribers). Rather,
published messages are characterized into channels, without knowledge of what (if any) subscribers
there may be. Subscribers express interest in one or more channels, and only receive messages that
are of interest, without knowledge of what (if any) publishers there are. This decoupling of publishers
and subscribers can allow for greater scalability and a more dynamic network topology.

I can use pubsub to play post message to different instances of the server side application without
care about which one is connect to the server.

In the future, MySQL or other relationship database will be use to ensure the data is safe, but it is
just for backup datas. The application will still run without MySQL. With this, sqlalchemy will be
use to connect MySQL.

.. _CoffeeScript: http://coffeescript.org/
.. _Python: http://python.org/
.. _Backbone: http://backbonejs.org/
.. _jQuery: https://jquery.org/
.. _less.css: http://www.lesscss.net/
.. _Handlebars: http://handlebarsjs.com/
.. _grunt: http://gruntjs.com/
.. _SoundManager: http://www.schillmania.com/projects/soundmanager2/
.. _Flask: http://flask.pocoo.org/
.. _Gevent: http://www.gevent.org/
.. _gevent_socketio: https://gevent-socketio.readthedocs.org/en/latest/
.. _redis: http://redis.io/


Conclusion
===================================

Music Service is the future of the music play.

In the future, consumers will have access to a full selection of music from online
services. It will be hard to choose which music to listen. The recommendation
algorithm will solve some of the problem, but not everyone want get music from
machine, they want to get new music from their friends or other people. So listening
to music will be more social.


