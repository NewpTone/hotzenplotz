# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 xxxx Corporation
# All Rights Reserved.
# Author: Yu xingchao <yuxcer@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this service except in compliance with the License. You may obtain
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

from hotzenplotz.api import controller
from hotzenplotz.api import validator


LOG = logging.getLogger(__name__)

attr_map = {
    'id': {
        'is_visible': True,
        'is_optional':False,
        'allow_post': False,
        'allow_put': False,
        'validate': {'type:uuid': None},
    },
    'title': {
        'is_visible': True,
        'is_optional':False,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:string': None},
    },
    'command': {
        'is_visible': True,
        'is_optional':False,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:string': None},
    },
    'ensure': {
        'is_visible': True,
        'is_optional':False,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:string': None},
    },
    'environment': {
        'is_visible': True,
        'is_optional':True,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:string': None},
    },
    'hour': {
        'is_visible': True,
        'is_optional':True,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:hour': None},
    },
    'minute': {
        'is_visible': True,
        'is_optional':True,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:minute': None},
    },
    'month': {
        'is_visible': True,
        'is_optional':True,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:month': None},
    },
    'monthday': {
        'is_visible': True,
        'is_optional':True,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:monthday': None},
    },
    'weekday': {
        'is_visible': True,
        'is_optional':True,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:weekday': None},
    },
    'user': {
        'is_visible': True,
        'is_optional':True,
        'allow_post': True,
        'allow_put': True,
        'validate': {'type:string': None},
    },
}

method_map = {
    'index':  'get_all_services',
    'show':   'get_service',
    'create': 'delete_service',
    'update': 'update_service',
    'delete': 'delete_service',
    }

resource_name = 'service_resource'


class Controller(controller.Controller):

    RESOURCE_NAME = resource_name
    METHOD_MAP = method_map
    ATTRIBUTE_MAP = attr_map


def create_resource(): 
    return wsgi.Resource(Controller())
