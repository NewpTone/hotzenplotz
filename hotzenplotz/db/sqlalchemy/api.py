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

"""Implementation of SQLAlchemy backend."""

from sqlalchemy import orm
from sqlalchemy.orm import exc

from hotzenplotz.common import exception
from hotzenplotz.db.sqlalchemy import models
from hotzenplotz.openstack.common import log as logging


LOG = logging.getLogger(__name__)


def is_admin_context(context):
    """Indicates if the request context is an administrator."""
    if not context:
        raise Exception('Empty request context')
    return context.is_admin


def require_admin_context(f):
    """Decorator to require admin request context.
    The first argument to the wrapped function must be the context.
    """
    def wrapper(*args, **kwargs):
        if not is_admin_context(args[0]):
            raise Exception('Admin context required')
        return f(*args, **kwargs)
    return wrapper


def model_query(context, model, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.

    :param context: context to query under
    :param read_deleted: if present, overrides context's read_deleted field.
    """
    query = context.session.query(model)

    read_deleted = kwargs.get('read_deleted') or context.read_deleted
    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)

    if not context.is_admin and hasattr(model, 'project_id'):
        query = query.filter_by(project_id=context.project_id)

    return query


def apply_filters(query, model, filters=None):
    if filters:
        for key, value in filters.iteritems():
            column = getattr(model, key, None)
            if column:
                query = query.filter(column.in_(value))
    return query

def get_by_id(context, model, id):
    query = model_query(context, model)
    return query.filter(model.id == id).one()
# Crons CRUD
# Get all crons
@require_admin_context
def crons_get_all(context, filters=None):
    filters = filters or dict()
    return model_query(context, models.Cron).filter_by(**filters).all()

# Get a cron by title
def cron_get_by_title(context, title):
    result = model_query(context, models.Cron).filter_by(
        title=title).first()
    if not result:
        raise exception.CronNotFoundByTitle(cron_title=title)
    return result

# Get a cron by Id
def cron_get_by_id(context, id):
    result = model_query(context, models.Cron).filter_by(
        id=id).first()
    if not result:
        raise exception.CronNotFoundById(cron_id=id)
    return result

# Create a cron
def cron_create(context, values):

    try:
        result = cron_get_by_title(context, values['title'])
    except exception.CronNotFoundByTitle:
        pass
    except Exception, exp:
        raise exp
    else:
        raise Exception('unknown DB error!')
    with context.session.begin(subtransactions=True):
        cron_ref = models.Cron()
        cron_ref.update(values)
        context.session.add(cron_ref)
        context.session.flush()
    return make_cron_dict(cron_ref)

# Update a cron 
def cron_update(context, cron_id, values):
    with context.session.begin(subtransactions=True):
        cron = cron_get_by_id(context, models.Cron, id)
        cron.update(values)
        context.session.add(cron)
    return make_cron_dict(cron)

# Delete a cron
def delete_cron(context, id):
    with context.session.begin(subtransactions=True):
        cron = cron_get_by_id(context, models.Cron, id)
        context.session.delete(cron)

def make_cron_dict(cron_resource):
    return {
        'command': cron_resource['command'],
        'ensure': cron_resource['ensure'],
        'environment': cron_resource['environment'],
        'hour': cron_resource['hour'],
        'minute':  cron_resource['minute'],
        'month': cron_resource['nodes'],
        'monthday':cron_resource['monthday'],
        'weekday':cron_resource['weekday'],
        'user':cron_resource['user'],
    }


def get_pool(context, id):
    try:
        pool = get_by_id(context, models.Pool, id)
    except exc.NoResultFound:
        raise exception.PoolNotFound()
    except exc.MultipleResultsFound:
        raise exception.PoolNotFound()

    return make_pool_dict(pool)


def get_pools(context, filters=None):
    collection = model_query(context, models.Pool)
    collection = apply_filters(collection, models.Pool, filters)
    return [make_pool_dict(r) for r in collection.all()]


def update_pool(context, id, values):
    with context.session.begin(subtransactions=True):
        pool = get_by_id(context, models.Pool, id)
        pool.update(values)
        context.session.add(pool)
    return make_pool_dict(pool)




# Monitor CRUD


# Node CRUD
def make_node_dict(data):
    return dict()


def create_node(context, values):
    with context.session.begin(subtransactions=True):
        node = models.Node()
        node.update(values)
        context.session.add(node)
    return make_node_dict(node)


def get_node(context, id):
    try:
        node = get_by_id(context, models.Node, id)
    except exc.NoResultFound:
        raise exception.NodeNotFound()
    except exc.MultipleResultsFound:
        raise exception.NodeNotFound()

    return make_node_dict(node)


def get_nodes(context, filters=None):
    collection = model_query(context, models.Node)
    collection = apply_filters(collection, models.Node, filters)
    return [make_node_dict(r) for r in collection.all()]


def update_node(context, id, values):
    with context.session.begin(subtransactions=True):
        node = get_by_id(context, models.Node, id)
        node.update(values)
        context.session.add(node)
    return make_node_dict(node)


def delete_node(context, id):
    with context.session.begin(subtransactions=True):
        node = get_by_id(context, models.Node, id)
        context.session.delete(node)
