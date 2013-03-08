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
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy.ext import declarative

from hotzenplotz.openstack.common import timeutils

BASE = declarative.declarative_base()


class DictBase(object):
    """Base class for Puppet Resource Models."""
    __table_args__ = {'mysql_engine': 'InnoDB'}
    created_at = sql.Column(sql.DateTime, default=timeutils.utcnow)
    updated_at = sql.Column(sql.DateTime, onupdate=timeutils.utcnow)
    deleted_at = sql.Column(sql.DateTime)
    deleted = sql.Column(sql.Boolean, default=False)
    id = sql.Column(sql.String(36), primary_key=True)
    user_id = sql.Column(sql.String(255), nullable=False)
    tenant_id = sql.Column(sql.String(255), nullable=False)
    title = sql.Column(sql.String(255), default=None)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        self._i = iter(orm.object_mapper(self).columns)
        return self

    def next(self):
        n = self._i.next().name
        return n, getattr(self, n)

    def update(self, values):
        """Make the model object behave like a dict"""
        for k, v in values.iteritems():
            setattr(self, k, v)

    def iteritems(self):
        """Make the model object behave like a dict.
        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                       if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()


class Cron(BASE, DictBase):
    """Represents cron resource."""

    __tablename__ = 'crons'
    command = sql.Column(sql.String(255), default=None)
    ensure = sql.Column(sql.String(8), default='present')
    environment = sql.Column(sql.String(255), default=None)
    hour = sql.Column(sql.String(16), default=None)
    minute = sql.Column(sql.String(16), default=None)
    month = sql.Column(sql.Integer(2), default=None)
    monthday = sql.Column(sql.Integer(2), default=None)
    weekday = sql.Column(sql.Integer(2), default=None)
    user = sql.Column(sql.String(32), default=None)


class Execs(BASE, DictBase):
    """Represents exec resource."""

    __tablename__ = 'execs'
    create = sql.Column(sql.String(255),default=None)
    cwd = sql.Column(sql.String(128),default=None)
    environment = sql.Column(sql.String(255),default=None)
    group = sql.Column(sql.String(16),default=None)
    user = sql.Column(sql.String(32),default=None)
    logoutput = sql.Column(sql.String(10),default=None)
    onlyif = sql.Column(sql.String(500),default=None)
    path = sql.Column(sql.String(255),default=None)
    refresh = sql.Column(sql.String(255),default=None)
    refreshonly = sql.Column(sql.Boolean,default=False)
    unless  = sql.Column(sql.String(500),default=None)


class Files(BASE, DictBase):
    """Represents file resource."""

    __tablename__ = 'files'
    path = sql.Column(sql.String(255), default=None)
    content = sql.Column(sql.String(500), default=None)
    ensure = sql.Column(sql.String(16), default=None)
    group = sql.Column(sql.String(16),default=None)
    owner = sql.Column(sql.String(16),default=None)
    mode = sql.Column(sql.String(8),default=None)
    source = sql.Column(sql.String(255),default=None)
    target = sql.Column(sql.String(255),default=None)
    recurse = sql.Column(sql.String(8).default=None)
    #group = orm.relationship("Monitor", backref=orm.backref("pool"))


class Groups(BASE, DictBase):
    """Represents group resource."""

    __tablename__ = 'groups'
    #pool_id = sql.Column(sql.String(36), sql.ForeignKey('pools.id'))
    name = sql.Column(sql.String(64), default=None)
    members = sql.Column(sql.String(255), default=None)   
    ensure = sql.Column(sql.String(16), default=None)  


class Packages(BASE, DictBase):
    """Represents package resource."""

    __tablename__ = 'resources'
    name = sql.Column(sql.String(64), default=None)
    ensure = sql.Column(sql.String(16), default=None)
    source = sql.Column(sql.String(128), default=True)

class Services(BASE, DictBase):
    """Represents service resource."""

    __tablename__ = 'services'
    enable = sql.Column(sql.String(8),default=None)
    ensure = sql.Column(sql.String(16), default=None)
    hasrestart = sql.Column(sql.Boolean(),default=False)
    hasstatus = sql.Column(sql.Boolean(),default=Fasle)
    name = sql.Column(sql.String(64), default=None)
    path = sql.Column(sql.String(255), default=True)
class User(BASE, DictBase):
    """Represents user resource."""

    __tablename__ = 'users'
    name = sql.Column(sql.String(64), default=None)
    ensure = sql.Column(sql.String(16), default=None)
    gid = sql.Column(sql.String(64), default=None)
    groups = sql.Column(sql.String(64),default=None)
    home = sql.Column(sql.String(64),default=None)
    managehome = sql.Column(sql.Boolean(),default=True)
    password = sql.Column(sql.String(32),default=None)
    shell = sql.Column(sql.String(32),default=None)
    system = sql.Column(sql.boolean(),default=False)

