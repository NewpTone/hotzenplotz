# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 xxxx Corporation
# All Rights Reserved.
# Author: Yu xingchao <yuxcer@gmail.com>
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
"""
Controller framework
"""

from hotzenplotz.openstack.common import cfg
from hotzenplotz.openstack.common import log as logging
from hotzenplotz.openstack.common import wsgi

from hotzenplotz.api import api
from hotzenplotz.common import context

LOG = logging.getLogger(__name__)

class ZmqClient(object):
    """0MQ Client used Request-Reply mode.
    """
    def __init__(self, host='127.0.0.1', port=8664):
        url = "tcp://%s:%s" % (host, port)
        context = zmq.Context()
        self.handler = context.socket(zmq.REQ)
        self.handler.connect(url) 
    def __del__(self):
        self.handler.close()

    def call(self, msg_body):
        self.handler.send_json(msg_body)
        msg_body = self.handler.recv_json()
        return jsonutils.loads(msg_body)

class Controller(object):

#    def __init__(self, resource_name=None, attribute_map=None, method_map=None):
#        import pdb; pdb.set_trace()
#        self.resource_name = resource_name
#        self.attribute_map = attribute_map
#        self.method_map    = method_map 
        #self.client = ZmqClient(host=cfg.CONF.server_listen,
        #                      port=cfg.CONF.server_listen_port)
    def __init__(self):
        super(Controller, self).__init__()

    def verify_request(self, context, req, body):
        """verifies required attributes are in request"""
        pass

    def index(self, req, **kwargs):
        """Returns a list of the required entities"""
        LOG.info(req.environ['hotzenplotz.context'])
        context = req.environ['hotzenplotz.context']
        method = self.METHOD_MAP['index']
        args = { 
                'user_id': context.user_id,
                'project_id': context.project_id,
                'is_admin': context.is_admin,
                'all_tenants': False,
        }   
        method_func = getattr(api, method)
        result = method_func(context, **args)
        return result

    def show(self, req, id, **kwargs):
        """Return detailed information about the requested entity"""
        import pdb; pdb.set_trace()
        LOG.info(req.environ['hotzenplotz.context'])
        context = req.environ['hotzenplotz.context']
        method = self.METHOD_MAP['show']
        args = {
                'user_id': context.user_id,
                'project_id': context.project_id,
                'id': id, 
               }  
        LOG.debug(args)
        method_func = getattr(api, method)
        result = method_func(context, **args)
        return result

    def create(self, req, body=None, **kwargs):
        """Create a new instance of the requested entity"""
        LOG.info(req.environ['hotzenplotz.context'])
        context = req.environ['hotzenplotz.context']
        zmq_args = {
            'method': self.METHOD_MAP['create'],
            'args': {
                'user_id': context.user_id,
                'project_id': context.project_id,
            },
        }
        resource_info = body[self.resource_name]
        zmq_args['args'].update(resource_info)
        LOG.debug(zmq_args)
        result = self.client.call(zmq_args)
        return result

    def update(self, req, id, body=None, **kwargs):
        """Update the specified entity's attributes"""
        LOG.info(req.environ['hotzenplotz.context'])
        context = req.environ['hotzenplotz.context']
        zmq_args = {
            'method': self.METHOD_MAP['update'],
            'args': {
                'user_id': context.user_id,
                'project_id': context.project_id,
                'uuid': id,
            },
        }
        resource_info = body[self.resource_name]
        zmq_args['args'].update(resource_info)
        LOG.debug(zmq_args)
        result = self.client.call(zmq_args)
        return result

    def delete(self, req, id, **kwargs):
        """Delete the specified entity"""
        LOG.info(req.environ['hotzenplotz.context'])
        context = req.environ['hotzenplotz.context']
        zmq_args = {
            'method': self.METHOD_MAP['update'],
            'args': {
                'user_id': context.user_id,
                'project_id': context.project_id,
                'is_admin': context.is_admin,
                'uuid': id,
            },
        }
        LOG.debug(zmq_args)
        result = self.client.call(zmq_args)
        return result

