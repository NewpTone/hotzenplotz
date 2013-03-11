# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Ustack Corporation
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

import eventlet
import zmq

from hotzenplotz.openstack.common import jsonutils
from hotzenplotz.openstack.common import log as logging

from hotzenplotz import db
from hotzenplotz import manager
from hotzenplotz.common import context
from hotzenplotz.common import flags
from hotzenplotz.common import utils
from hotzenplotz.server import api
from hotzenplotz.server import state

FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)


def client_routine(*args, **kwargs):
    """Handler api and client's request
    """
    LOG.info('hotzenplotz client starting...')
    handler = kwargs['handler']

    while True:
        eventlet.sleep(0)
        socks = dict(poller.poll(100))
        if socks.get(handler) == zmq.POLLIN:
            msg_type, msg_uuid, msg_json = handler.recv_multipart()
            response = dict()
            cli_msg = {'code': 200, 'message': 'OK'}
            try:
                msg_body = jsonutils.loads(msg_json)
                LOG.debug("<<<<<<< client: %s" % msg_body)
                method = msg_body['method']
                args = msg_body['args']
                ctxt = context.get_context(**args)
                method_func = getattr(api, method)
                result = method_func(ctxt, **args)
                if result is not None:
                    response.update(result)
                # send request to worker
                try:
                    msg = api.get_msg_to_worker(ctxt, method, **args)
                    if msg is not None:
                        request_msg = jsonutils.dumps(msg)
                        LOG.debug(">>>>>>> worker: %s" % request_msg)
                        broadcast.send_multipart([msg_type, msg_uuid,
                                                  request_msg])
                except Exception:
                    pass
            except Exception as e:
                cli_msg['code'] = 500
                cli_msg['message'] = str(e)
                LOG.exception(cli_msg['message'])
            response.update(cli_msg)
            response_msg = jsonutils.dumps(response)
            LOG.debug(">>>>>>> client: %s" % response_msg)
            handler.send_multipart([msg_type, msg_uuid, response_msg])


def worker_routine(*args, **kwargs):
    LOG.info('hotzenplotz worker starting...')

    feedback = kwargs['feedback']
    poller = zmq.Poller()
    poller.register(feedback, zmq.POLLIN)

    while True:
        eventlet.sleep(0)
        socks = dict(poller.poll(100))
        if socks.get(feedback) == zmq.POLLIN:
            msg_type, msg_uuid, msg_json = feedback.recv_multipart()
            msg_body = jsonutils.loads(msg_json)
            LOG.debug("<<<<<<< worker: %s" % msg_body)
            # update load balancer's state
            try:
                args = msg_body
                ctxt = context.get_admin_context()
                api.update_load_balancer_state(ctxt, **args)
            except Exception as exp:
                LOG.exception(str(exp))
                continue

class ServerManager(manager.Manager):

    def __init__(self):
        super(ServerManager, self).__init__()

    def init_host(self):
        """Handle initialization if this is a standalone service.

        Child class should override this method

        """
        self.pool = eventlet.GreenPool(3)

    def start(self):
        zmq_context = zmq.Context()

        # Socket to receive messages on
        handler = zmq_context.socket(zmq.REP)
        handler.bind("tcp://%s:%s" % (FLAGS.server_listen,
                                      FLAGS.server_listen_port))

        args = {
            'handler': handler,
        }

        self.pool.spawn(client_routine, **args)
        self.pool.spawn(worker_routine, **args)

    def wait(self):
        self.pool.waitall()
