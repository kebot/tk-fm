.. 开题报告

=====================================
UNDERGRADUATE THESIS PROJECT PROPOSAL
=====================================

---------------------------------------------
The design and optimization of the Turkey FM
---------------------------------------------

:Author: Keith Yao (International College, Zhejiang University of Technology)


.. Table of contents will generated by sphinx

Abstract
========

.. 现在, 越来越多的人开始, 从Paradro 开始, 越来越多的网站开始基于用户的反馈推荐歌曲
   针对个人的歌曲推荐 Douban Radio

   但是, 忽略了公共场合播放的音乐往往不堪入耳. 人们需要在公共场合更有针对性地听到自己想听的音乐.

   商家也可以通过次吸引更多的用户.

We have so many products that let us listen to music along. In the past(过去),
people listen to the music from CD, MP3. Now, more and more people starting
play their music from online services. This services will record your favourite
songs, your play history and song you don't like. And then they will play some
'new' songs that you may like.

With this project, guests simple use their mobile phones to connect to our service,
the service will choose the music they may all like.


**Keyword**: *music* *real-time*

Glossary
========
What follows is a list of definitions for terms that may be useful when reading this proposal.


.. TODO 名词解释


Rationale and Objectives
===========================

The project name is `Turkeyfm`, and it's just a name.

Music keeps your right brain happy while your left brain works.
My company is a pretty musical company.

We built an employee-driven geographically-distributed, multi-client, HTML5-based,

A shared music server.

Music has been a fun part of ...whatever.

Just saying: Glass, next song.

We use whatever music player to play music and share it with our friends in the
sameroom. Consider these:

if someone play the music, and you don't like it, you want to skip the song,
what did you do?

if you want to play the music.

Here comes the problem with traditional music player.


Rationable
----------

At the present, people wanted to have a simple way to share the music they love
with others. They will play the music they like with other people. Others has no
chance to choose the song they like, they will be boring to this.

I try to solve this problem by using iTunes Remote(you can find it in App Store),
it will let other guest to control the music playing in one's iTunes. It solves
the problem, but it can only use in iOS devices.

This project will run on almost all platforms, so I decides to make a webbased
client for the project.

Another problem I meet is all the song is stored in iTunes, it means if your fav
song is not in the iTunes library, you have no chance to hear that. My solution
is build a music service to record and store songs, it will meet some copyright
problem.
So I decided to build it with some websites that already solved the copyright
problem.

Another feature I will support in this project is live-sync playing position
and playing song with different people. It will help friends didn't live in
one room to share their music with each other.

Objectives
----------
In order to achieve the target above, a user friendly user interface and a
server will be developed.

In the client side, a beautiful user interface will be designed. It can be run
on almost every devices including: Desktop Web Browser, iOS, Android, Windows Phone
and other web browsers. It will support html5 audio or flash to play the music
on the web.

The application is room based, a room is whether a room exists in real world or a
virtual room that only exists in the network.

User can choose one room to join, or create a new room to starting music playing.
If the user didn't choose what song will be played, the music will not be stopped,
the music server will recommend a random song to play. User can interaction with
the application if they like/hate the song. And then the server will recommend more
song that meet the taste that in the room. In addition, users are able to skip the
song or add some song to the songlist.

The server side is the heart of the application. It provide some ways to keep
all users in one room has the same player position. And the server must provide
song recommend service and a big some library. Fortunately, the internet already
has some online music service that can help.

Except song and room related services, the server also provate user related service
including user registration, device recognise(if the user both login with iPhone and
iPad, the server can distinguish them).


Preliminary Impact Statement
============================

In order to simplify cross platform problem, webkit based UI is the best choice for
this project. The web platform can connect to the server and show the UI that can be
interaction with end point user. The common way to connect between server and client
is ajax(http request), but in html5, another protocal called websocket can be use in
this project.

The song library is also the problem, SoundCloud provide lots of songs. I also choose
another music service called douban.fm to provide and music service. DoubanFM provide
a music recommend service that user can get more interesting songs by interaction with
the music service. So I need to do some job to let user interaction with some music
recommend service.

After that, I will use some technogy to sync between different users in the same room,
I will define some message types and do some message passing.

Review Of Relevant Literature
=============================

The exsiting site that provide online music service
---------------------------------------------------

There are several business models in the online audio digital platforms and while
I don't know all of the companies you listed above here are some broad strokes:

Playlist Service: This would be Rdio & Spotify.  These are services that rely upon users creating a list of songs and then sharing that list & music with others so essentially a self-curated DJ approach that you can share with others.  This allows others to learn of new music/groups and appreciate the brilliance of their fellow (wo)man if they aren't themselves musically inclined but appreciate some good beats. Oftentimes, the playlists are categorized by format (like we typically think of a broadcast station) or by mood (Going Out music, Exercise music, etc).

Personalized Radio: In the U.S., two larger services are Pandora and iHeartRadio.  These allow you to type in an artist(s) or song(s) you'd like to hear and they will play something along that line...due to royalty issues they may not be able to play the exact song/artist requested (hence radio not playlist) but it is personalized due to them creating a station using your expressed preference.

Online Radio: This is a radio station only available via the internet (unlike the category below) but is not curated to your specific preference but is being DJ'd by someone else.  The logic being that a professional who knows the music will be able to create a better listening experience than someone who doesn't have that background.  Oftentimes, these stations are categorized by format (like we typically think of a broadcast station) or by mood (Going Out music, Exercise music, etc). 

Streaming Radio: This label is used a lot to represent alot of different things but I consider it to mean it is a broadcast station that is being streamed online. Thus it isn't personalized to you but instead you are hearing what everyone else is hearing in the station's market. So, in the states, it would be station WXYZ-FM based out of Anytown, USA but coming through the internet rather than your radio.

Hybrid models: Many of services do a couple of the above; for example iHeartRadio allows you to stream any Clear Channel radio station (streaming radio), or instead listen to an internet only station (Road Trip Radio station), or pick an artist to build a your own station (Personalized Radio) while www.mog.com allows you to do either personalized radio or playlists...

Revenue Models: This has been a tough nut to crack for all these audio services as it has low barrier of entry (i.e. anyone can setup a platform to play music online) and music is already free and ubiquitous via broadcast radio and listeners' own music collection. 

BUT generally speaking the revenue model is a hybrid of: use the service for free but get ads (so ads become their revenue) or pay them a monthly subscription ($5-$10/month seems the average) and you'll get no ads (making subscription their revenue).  Generally speaking, the  vast majority of these services are finding their revenues are coming from ads as people seem reluctant to pay for a subscription.

HTTP Push Technology Overview
----------------------------------------------------

Long Polling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Long polling is itself not a true push; long polling is a variation of the
traditional polling technique, but it allows emulating a push mechanism under
circumstances where a real push is not possible.
With long polling, the client requests information from the server in a way similar
to a normal polling; however, if the server does not have any information available
for the client, then instead of sending an empty response, the server holds the
request and waits for information to become available (or for a suitable timeout
event), after which a complete response is finally sent to the client.
For example, BOSH is a popular, long-lived HTTP technique used as a long-polling
alternative to TCP when TCP is difficult or impossible to employ directly (e.g., 
in a web browser);[9] it is also an underlying technology in the XMPP, which Apple
uses for its iCloud push support.

WebSocket
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WebSocket is a web technology providing full-duplex communications channels over
a single TCP connection. The WebSocket protocol was standardized by the IETF as
RFC 6455 in 2011, and the WebSocket API in Web IDL is being standardized by the
W3C.


Comet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comet is a web application model in which a long-held HTTP request allows a web
server to push data to a browser, without the browser explicitly requesting it.

Comet is an umbrella term, encompassing multiple techniques for achieving this
interaction. All these methods rely on features included by default in browsers,
such as JavaScript, rather than on non-default plugins. The Comet approach
differs from the original model of the web, in which a browser requests a
complete web page at a time.

The use of Comet techniques in web development predates the use of the word Comet
as a neologism for the collective techniques. Comet is known by several other
names, including Ajax Push, Reverse Ajax, Two-way-web, HTTP Streaming, and HTTP
server push among others.


Technology Choosen
==================

The main programing language is Python and CoffeeScript.

The project is not simple web based and database-driven. So php is not
the choice, and Java is so 'heavy', I don't like it. And I love Python.

What is CoffeeScript?

CoffeeScript is a little language that compile to JavaScript. And it is
JavaScript, but it has better syntax.

Where you store your datas?

Redis is the only 'Database' I use, it is a simple key-value data-structure
server.

I use Flask and gevent-websocket to build two kinds of services. The webserver
is gevent based. Nginx will be use to handle static files.

Socket.IO is used for wrap websocket and for better browser support.

In browser Backbone helps build MVC application. jQuery and other libs to help
build beautiful web-application.

Above are the technology I use in this project.

Server-side:

  Background worker part, a background worker that handle all background work.

  Real-time server is a web-socket based server that serves all room-based requests.

  Web-server handle normal web-requests

Client-side:

  The client side is Mobile friendly web based application.
  In mobile side, use PhoneGap to wrap all page to a app.


Statement Of Project Activities
================================

In order to complete my project, a detailed description about activities and an
associated schedule are privided.


Activities
-----------

The activities described the outline of steps I plan to take to complete my project.
The time arrangement is only estimated and each section may take more
or less time to complete depending on my proficiency in each and the actual difficulty
of the task.

Background Information
~~~~~~~~~~~~~~~~~~~~~~~

I have to understand what I plan to do, and what will be the most hard ascept of my
project. Which language will I choose? Which framework and libs will be choosen.

Gather User Requirement Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~

I will discuess my idea with some friends to ensure what they really want when listen
to the music. And discover the way to solve the problem.

Design the user interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I will omnifocus to design the user interface of the project, make sure what will happen
when the user click here. And what will show on the screen.


Design the Message Model for the application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's more important to design the message passing model than the data store model.
In this application, messages will be passing from one user to another user through
the server. How to make it most effective? It's a big problem, how to make every
client have the same data model and songlist in the same room. This is what I need
to consider carefully.


Writing the code
~~~~~~~~~~~~~~~~~~

Just writing code, it's easy for me.

Create test application
~~~~~~~~~~~~~~~~~~~~~~~

Test your application with machine and friends.

Post it to the internet
~~~~~~~~~~~~~~~~~~~~~~~~

Make it online, make it possiable to serve others.


Schedule
-------------

I have post all my schedule on trello.




