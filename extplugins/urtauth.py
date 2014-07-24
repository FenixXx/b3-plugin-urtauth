#
# UrT Auth Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2013 Daniele Pantaleone <fenix@bigbrotherbot.net>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
# CHANGELOG
#
# 24/07/2014 - 1.0   - Fenix - initial release
# 24/07/2014 - 1.0.1 - Fenix - fixed 'maxlevel' config value not being loaded

__author__ = 'Fenix'
__version__ = '1.0.1'


import b3
import b3.plugin
import b3.events

from b3.functions import getCmd
from ConfigParser import NoOptionError

class UrtauthPlugin(b3.plugin.Plugin):

    adminPlugin = None      # admin plugin instance

    settings = {
        'maxlevel': 2,
        'reason': '^7you need an ^1auth ^7account to play here'
    }

    ####################################################################################################################
    ##                                                                                                                ##
    ##   STARTUP                                                                                                      ##
    ##                                                                                                                ##
    ####################################################################################################################

    def __init__(self, console, config=None):
        """
        Object constructor.
        """
        b3.plugin.Plugin.__init__(self, console, config)
        if self.console.gameName != 'iourt42':
            self.critical("unsupported game : %s" % self.console.gameName)
            raise SystemExit(220)

        # get the admin plugin
        self.adminPlugin = self.console.getPlugin('admin')
        if not self.adminPlugin:
            self.critical('could not start without admin plugin')
            raise SystemExit(220)

        self.timers = {}

    def onLoadConfig(self):
        """
        Load plugin configuration.
        """
        try:
            self.settings['maxlevel'] = self.console.getGroupLevel(self.config.get('settings', 'maxlevel'))
            self.debug('loaded settings/maxlevel: %s' % self.settings['maxlevel'])
        except NoOptionError:
            self.warning('could not find settings/maxlevel in config file, using default: %s' % self.settings['maxlevel'])
        except ValueError, e:
            self.error('could not load settings/maxlevel config value: %s' % e)
            self.debug('using default value (%s) for settings/maxlevel' % self.settings['maxlevel'])

        try:
            self.settings['reason'] = self.config.get('settings', 'reason')
            self.debug('loaded settings/reason: %s' % self.settings['reason'])
        except NoOptionError:
            self.warning('could not find settings/reason in config file, using default: %s' % self.settings['reason'])
        except KeyError, e:
            self.error('could not load settings/reason config value: %s' % e)
            self.debug('using default value (%s) for settings/reason' % self.settings['reason'])

    def onStartup(self):
        """
        Initialize plugin settings.
        """
        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = getCmd(self, cmd)
                if func:
                    self.adminPlugin.registerCommand(self, cmd, level, func, alias)

        # register the events needed
        self.registerEvent(self.console.getEventID('EVT_CLIENT_CONNECT'), self.onConnect)

        # notice plugin startup
        self.debug('plugin started')

    ####################################################################################################################
    ##                                                                                                                ##
    ##   EVENTS                                                                                                       ##
    ##                                                                                                                ##
    ####################################################################################################################

    def onEnable(self):
        """
        Executed on plugin enable.
        """
        # check auth on all the online clients
        for client in self.console.clients.getList():
            self.doAuthCheck(client)

    def onConnect(self, event):
        """
        Handle EVT_CLIENT_CONNECT.
        """
        # check the auth of the connecting client
        self.doAuthCheck(event.client)

    ####################################################################################################################
    ##                                                                                                                ##
    ##   OTHER METHODS                                                                                                ##
    ##                                                                                                                ##
    ####################################################################################################################

    def doAuthCheck(self, client):
        """
        Check that a client is authed using UrT 4.2 auth system (<pbid> field set).
        :param client: The client on who perform the check.
        """
        if not self.console.is_frozensand_auth_available():
            self.debug('skipping auth account check for %s<@%s> : auth system not available' % (client.name, client.id))
            return

        if client.maxLevel >= self.settings['maxlevel']:
            self.debug('skipping auth account check for %s<@%s> : he is a high level client' % (client.name, client.id))
            return

        # notice account check started
        self.debug('executing auth account check on %s<@%s> ...' % (client.name, client.id))

        if not client.pbid:
            # client is not authed and auth system is working: perform a kick
            self.debug('auth account check completed for %s<@%s> : client is NOT authed' % (client.name, client.id))
            client.kick(self.settings['reason'])
            return

        # client is correctly authed so let him stay online
        self.debug('auth account check completed for %s<@%s> : client is authed as <%s>' % (client.name, client.id, client.pbid))