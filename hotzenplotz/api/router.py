# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 xxxx Corporation
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

from hotzenplotz.api.resource import cron
from hotzenplotz.api.resource import Exec
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
        self.controller = {}
        self._setup_basic_routes(mapper)
        super(APIRouter, self).__init__(mapper)

    def _setup_basic_routes(self, mapper):
        mapper.redirect("", "/")
        
        #Cron Operations
        self.controller['cron'] = cron.create_resource()
        mapper.connect('/crons',
                       controller=self.controller['cron'],
                       action='index',
                       conditions=dict(method=['GET']))
        mapper.connect('/crons/{cron_id}',
                       controller=self.controller['cron'],
                       action='show',
                       conditions=dict(method=['GET']))
        mapper.connect('/crons',
                       controller=self.controller['cron'],
                       action='create',
                       conditions=dict(method=['POST']))
        mapper.connect('/crons/{cron_id}',
                       controller=self.controller['cron'],
                       action='update',
                       conditions=dict(method=['PUT']))
        mapper.connect('/crons/{cron_id}',
                       controller=self.controller['cron'],
                       action='delete',
                       conditions=dict(method=['DELETE']))
      
        #Exec Operations
        self.controller['exec'] = Exec.create_resource()
        mapper.connect('/execs',
                       controller=self.controller['exec'],
                       action='index',
                       conditions=dict(method=['GET']))
        mapper.connect('/execs/{exec_id}',
                       controller=self.controller['exec'],
                       action='show',
                       conditions=dict(method=['GET']))
        mapper.connect('/execs',
                       controller=self.controller['exec'],
                       action='create',
                       conditions=dict(method=['POST']))
        mapper.connect('/execs/{exec_id}',
                       controller=self.controller['exec'],
                       action='update',
                       conditions=dict(method=['PUT']))
        mapper.connect('/execs/{exec_id}',
                       controller=self.controller['exec'],
                       action='delete',
                       conditions=dict(method=['DELETE']))
        #import pdb; pdb.set_trace()
