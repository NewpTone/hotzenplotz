# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Sina Corporation
# All Rights Reserved.
# Author: Jiajun Liu <iamljj@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import routes

from hotzenplotz.openstack.common import wsgi
from hotzenplotz.openstack.common import log as logging

from hotzenplotz.api.resource import device
from hotzenplotz.api.resource import node
from hotzenplotz.api.resource import pool


LOG = logging.getLogger(__name__)


class APIRouter(wsgi.Router):
    """
    Base class for hotzenplotz API routes.
    """

    @classmethod
    def factory(cls, global_config, **local_config):
        return cls()

    def __init__(self):
        mapper = routes.Mapper()
        self.resources = {}
        self._setup_basic_routes(mapper)
        super(APIRouter, self).__init__(mapper)

    def _setup_basic_routes(self, mapper):
        mapper.redirect("", "/")

        self.resources['device'] = device.create_resource()
        mapper.resource('device', 'devices',
                        controller=self.resources['device'])

        self.resources['pool'] = pool.create_resource()
        mapper.resource('pool', 'pools',
                        controller=self.resources['pool'])

        self.resources['node'] = node.create_resource()
        mapper.resource('node', 'nodes',
                        controller=self.resources['node'])
        import pdb; pdb.set_trace()
