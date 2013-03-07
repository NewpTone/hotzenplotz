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
SQLAlchemy models for hotzenplotz data.
"""
import time

import sqlalchemy as sql
from sqlalchemy import exc
from sqlalchemy import orm
from sqlalchemy.engine import url

from hotzenplotz.openstack.common import cfg
from hotzenplotz.openstack.common import log as logging


LOG = logging.getLogger(__name__)

sql_opts = [
    cfg.StrOpt('sql_connection',
               default='mysql://root:2317@127.0.0.1:3306/hotzenplotz',
               help='Database connection'),
    cfg.IntOpt('sql_connection_debug',
               default=0,
               help='Verbosity of SQL debugging info, 0=None, 100=all'),
    cfg.IntOpt('sql_max_retries',
               default=10,
               help='Max retry times when database connection error occur'),
    cfg.StrOpt('reconnect_interval',
               default=3,
               help='Retry interval when database connection error occur'),
]

cfg.CONF.register_opts(sql_opts)

_MAKER = None
_ENGINE = None


class MySQLPingListener(object):

    """
    Ensures that MySQL connections checked out of the
    pool are alive.

    Borrowed from:
    http://groups.google.com/group/sqlalchemy/msg/a4ce563d802c929f
    """

    def checkout(self, dbapi_con, con_record, con_proxy):
        try:
            dbapi_con.cursor().execute('select 1')
        except dbapi_con.OperationalError, e:
            if e.args[0] in (2006, 2013, 2014, 2045, 2055):
                raise exc.DisconnectionError("Database server went away")
            else:
                raise


def is_connection_error(args):
    """Return True if error in connecting to db."""
    conn_err_codes = ('2002', '2003', '2006')
    for err_code in conn_err_codes:
        if args.find(err_code) != -1:
            return True
    return False


def get_engine():
    global _ENGINE
    if not _ENGINE:
        connection_dict = url.make_url(cfg.CONF.sql_connection)
        engine_args = {
            'pool_recycle': 3600,
            'echo': False,
            'convert_unicode': True,
        }

        # Map our SQL debug level to SQLAlchemy's options
        if cfg.CONF.sql_connection_debug >= 100:
            engine_args['echo'] = 'debug'
        elif cfg.CONF.sql_connection_debug >= 50:
            engine_args['echo'] = True

        if 'mysql' in connection_dict.drivername:
            engine_args['listeners'] = [MySQLPingListener()]

        _ENGINE = sql.create_engine(cfg.CONF.sql_connection, **engine_args)

        sql_max_retries = cfg.CONF.get('sql_max_retries', 3)
        reconnect_interval = cfg.CONF.get('reconnect_interval', 3)
        while True:
            try:
                _ENGINE.connect()
                break
            except exc.OperationalError as e:
                if not sql_max_retries or \
                        not is_connection_error(e.args[0]):
                    raise
                sql_max_retries -= 1
                time.sleep(reconnect_interval)
    return _ENGINE


def get_session(autocommit=True, expire_on_commit=True):
    """Helper method to grab session"""
    global _MAKER, _ENGINE
    if not _MAKER:
        engine = get_engine()
        _MAKER = orm.sessionmaker(bind=engine,
                                  autocommit=autocommit,
                                  expire_on_commit=expire_on_commit)
    return _MAKER()
