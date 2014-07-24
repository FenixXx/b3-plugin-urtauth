#
# UrT Auth  Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2013 Daniele Pantaleone <fenix@bigbrotherbot.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from mock import Mock
from mock import call
from textwrap import dedent
from mockito import when
from tests import logging_disabled
from tests import UrtauthTestCase


class Test_events(UrtauthTestCase):

    def setUp(self):

        UrtauthTestCase.setUp(self)

        with logging_disabled():
            from b3.fake import FakeClient

        # create some clients
        self.mike = FakeClient(console=self.console, name="Mike", guid="mikeguid", groupBits=1)
        self.mark = FakeClient(console=self.console, name="Mark", guid="markguid", groupBits=1, pbid='markguid')
        self.bill = FakeClient(console=self.console, name="Bill", guid="billguid", groupBits=2)


    def tearDown(self):
        self.mike.disconnects()
        self.bill.disconnects()
        self.mark.disconnects()
        UrtauthTestCase.tearDown(self)

    ####################################################################################################################
    ##                                                                                                                ##
    ##   TEST CASES                                                                                                   ##
    ##                                                                                                                ##
    ####################################################################################################################

    def test_client_connect_with_no_account_and_low_group(self):
        # GIVEN
        self.mike.kick = Mock()
        # WHEN
        self.mike.connects("1")
        # THEN
        self.assertEqual(1, self.mike.kick.call_count)
        self.mike.kick.assert_has_calls([call('^7you need an ^1auth ^7account to play here')])

    def test_client_connect_with_account_and_low_group(self):
        # GIVEN
        self.mark.kick = Mock()
        # WHEN
        self.mike.connects("1")
        # THEN
        self.assertEqual(0, self.mark.kick.call_count)

    def test_client_connect_with_no_account_but_high_group(self):
        # GIVEN
        self.bill.kick = Mock()
        # WHEN
        self.bill.connects("1")
        # THEN
        self.assertEqual(0, self.bill.kick.call_count)



