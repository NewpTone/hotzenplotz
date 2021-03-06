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

import zmq
import eventlet

from hotzenplotz.openstack.common import cfg
from hotzenplotz.openstack.common import jsonutils
from hotzenplotz.openstack.common import log as logging

from hotzenplotz import manager
from hotzenplotz.common import exception
from hotzenplotz.worker.driver import cron

LOG = logging.getLogger(__name__)
FLAGS = cfg.CONF

class WorkerManager(manager.Manager):

    def __init__(self):
        super(WorkerManager, self).__init__()

    def init_host(self):
        """Handle initialization if this is a standalone service.

        Child class should override this method

        """
        zmq_context = zmq.Context()
        self.pool = eventlet.GreenPool(1)
        self.handler = zmq_context.socket(zmq.REP)

    def start(self):

       # Socket to receive messages on
        self.handler.bind("tcp://%s:%s" % (FLAGS.worker_listen,
                                      FLAGS.worker_listen_port))
        self.cronhandler = cron.CronHandler()

    def wait(self):
        
        LOG.info('hotzenplotz worker starting...')
        expect_keys=['cron_resource']
        while True:
            if self.handler.poll(5000):
                message = self.handler.recv_json()
            # check input message
                if not message.keys() or (message.keys()[0] not in expect_keys):
                    LOG.warn("Error. No resource type in message")
                    response_msg['code'] = 500
                    response_msg['message'] = "missing resource type field"

                    self.handler.send_json(response_msg)
                    break
                 #response_msg = {'code': 200, 'message': 'OK'}
                if message['cron_resource']:
                    try:
                        self.cronhandler.do_config(message)
                    except exception.CronError, e:
                        response_msg['code'] = 500
                        response_msg['message'] = str(e)
                elif message['exec_resource']:
                    try:
                        self.cron_resrouce.do_config(message)
                    except exception.HaproxyConfigureError, e:
                        response_msg['code'] = 500
                        response_msg['message'] = str(e)
                else:
                    LOG.exception('Error. Unsupported protocol')
                    response_msg['code'] = 500
                    response_msg['message'] = "Error: unsupported protocol"

            else:
                pass    
