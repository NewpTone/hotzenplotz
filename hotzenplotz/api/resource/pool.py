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

from hotzenplotz.openstack.common import log as logging
from hotzenplotz.openstack.common import wsgi

from hotzenplotz import db
from hotzenplotz.api import controller


LOG = logging.getLogger(__name__)


pool_attr_map = {
    'id': {
        'is_visible': True,
        'allow_post': False,
        'allow_put': False,
        'validate': {'type:uuid': None},
    },
    'name': {
        'is_visible': True,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:string': None},
    },
}

class Controller(controller.Controller):

    RESOURCE_NAME = "pool"
    ATTRIBUTE_MAP = pool_attr_map

    def index(self, req, **kwargs):
        """Returns a list of the required entities"""

        context = req.environ['hotzenplotz.context']
        return db.get_pools(context, **kwargs)


def create_resource():
    return wsgi.Resource(Controller())
