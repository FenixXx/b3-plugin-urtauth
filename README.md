UrT Auth Plugin for BigBrotherBot [![BigBrotherBot](http://i.imgur.com/7sljo4G.png)][B3]
=================================

Description
-----------

A [BigBrotherBot][B3] plugin which increase the functionality of UrT 4.2 auth system. The plugin will prevent NOT authed 
people to connect to your game server if their group level is lower than the one specified in the configuration file. This
introduces the possibility of letting some people play unauthed on your server (mostly well known players) while new players
are required to login on the UrT 4.2 auth system to stay online.

Download
--------

Latest version available [here](https://github.com/danielepantaleone/b3-plugin-urtauth/archive/master.zip).

Installation
------------

* copy the `urtauth.py` file into `b3/extplugins`
* copy the `plugin_urtauth.ini` file in `b3/extplugins/conf`
* add to the `plugins` section of your `b3.xml` config file:

  ```xml
  <plugin name="urtauth" config="@b3/extplugins/conf/plugin_urtauth.ini" />
  ```
  
Requirements
------------

* Urban Terror 4.2
* B3 [version >= 1.10dev]

Support
-------

If you have found a bug or have a suggestion for this plugin, please report it on the [B3 forums][Support].

[B3]: http://www.bigbrotherbot.net/ "BigBrotherBot (B3)"
[Support]: http://forum.bigbrotherbot.net/plugins-by-fenix/urt-auth-plugin// "Support topic on the B3 forums"

[![Build Status](https://travis-ci.org/danielepantaleone/b3-plugin-urtauth.svg?branch=master)](https://travis-ci.org/danielepantaleone/b3-plugin-urtauth)
