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

"""
Routines for config hotzenplotz
"""
import os
import sys

from paste import deploy

from hotzenplotz.openstack.common import cfg
from hotzenplotz.openstack.common import log as logging


LOG = logging.getLogger(__name__)

core_opts = [
    cfg.StrOpt('state_path',
               default='/var/lib/hotzenplotz',
               help='Top-level directory for maintaining hotzenplotz'),
    cfg.StrOpt('api_paste_config',
               default='api-paste.ini',
               help='paste configuration file'),
    cfg.StrOpt('auth_strategy',
               default='noauth',
               help='authorize strategy'),
    cfg.StrOpt('api_listen',
               default='127.0.0.1',
               help='IP address for hotzenplotz API to listen.'),
    cfg.IntOpt('api_listen_port',
               default=8664,
               help='Port for hotzenplotz API to listen.'),
    cfg.StrOpt('worker_listen',
               default='127.0.0.1',
               help='IP address for hotzenplotz Worker to listen.'),
    cfg.IntOpt('worker_listen_port',
               default=8665,
               help='Port for hotzenplotz Worker to listen.'),
]

cfg.CONF.register_opts(core_opts)


def parse_args(args=None):
    if not args:
        args = sys.argv[1:]
    cfg.CONF(args, project="hotzenplotz")


def setup_logging(conf):
    """
    Sets up the logging options for a log with supplied name

    :param conf: a cfg.ConfOpts object
    """
    product_name = "hotzenplotz"
    logging.setup(product_name)
    log_root = logging.getLogger(product_name).logger
    log_root.propagate = 0
    LOG.info(_("Logging enabled!"))


def load_paste_app(app_name):
    """
    Builds and returns a WSGI app from a paste config file.

    :param app_name: Name of the application to load
    :raises RuntimeError when config file cannot be located or
            application cannot be loaded from config file
    """

    config_file = cfg.CONF.find_file(cfg.CONF.api_paste_config)
    config_path = os.path.abspath(config_file)

    try:
        app = deploy.loadapp("config:%s" % config_path, name=app_name)
    except (LookupError, ImportError):
        msg = _("Unable to load %(app_name)s from "
                "configuration file %(config_path)s.") % locals()
        raise RuntimeError(msg)
    return app


def show_configs():
    LOG.debug(_("Configuration options gathered from config file:"))
    items = dict([(k, v) for k, v in cfg.CONF.items()
                  if k not in ('__file__', 'here')])
    for key, value in sorted(items.items()):
        LOG.debug("%(key)-30s = %(value)s" % {'key': key, 'value': value})
