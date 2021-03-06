"""
Copyright (c) 2012-2013 RockStor, Inc. <http://rockstor.com>
This file is part of RockStor.

RockStor is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

RockStor is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from rest_framework import status
from rest_framework.test import APITestCase
from mock import patch
from storageadmin.tests.test_api import APITestMixin


class OauthAppTests(APITestMixin, APITestCase):
    fixtures = ['fix1.json']
    BASE_URL = '/api/oauth_app'

    @classmethod
    def setUpClass(cls):
        super(OauthAppTests, cls).setUpClass()

        # post mocks
        cls.patch_set_token = patch('storageadmin.views.appliances.set_token')
        cls.mock_set_token = cls.patch_set_token.start()
        cls.mock_set_token.return_value = {}

    @classmethod
    def tearDownClass(cls):
        super(OauthAppTests, cls).tearDownClass()

    def test_get(self):

        # get base URL
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)

        # get base URL
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)

    def test_post_requests(self):

        # Existing application name
        data = {'name': 'cliapp'}
        response = self.client.post(self.BASE_URL, data=data)
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR,
                         msg=response.data)

        e_msg = ('application with name: cliapp already exists.')
        self.assertEqual(response.data['detail'], e_msg)

        # happy path
        data = {'name': 'AccessKey1'}
        response = self.client.post(self.BASE_URL, data=data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)

    def test_delete_requests(self):
        # delete application that does not exist
        access_key = 'invalid'
        response = self.client.delete('%s/%s' % (self.BASE_URL, access_key))
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR,
                         msg=response.data)

        e_msg = ('application(invalid) does not exist')
        self.assertEqual(response.data['detail'], e_msg)

        # invalid delete operation
        access_key = 'cliapp'
        response = self.client.delete('%s/%s' % (self.BASE_URL, access_key))
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR,
                         msg=response.data)

        e_msg = ('application(cliapp) cannot be deleted because it is used '
                 'internally by Rockstor. If you really need to delete it, '
                 'login as root and use /opt/rock-dep/bin/delete-api-key '
                 'command. If you do delete it, please create another one '
                 'with the same name as it is required by Rockstor '
                 'internally.')
        self.assertEqual(response.data['detail'], e_msg)

        # happy path
        # create before you delete
        data = {'name': 'AccessKey2'}
        response = self.client.post(self.BASE_URL, data=data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)

        access_key = 'AccessKey2'
        response = self.client.delete('%s/%s' % (self.BASE_URL, access_key))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)
