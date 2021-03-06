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

import webob.dec
import webob.exc

from hotzenplotz.openstack.common import cfg
from hotzenplotz.openstack.common import wsgi
from hotzenplotz.openstack.common import log as logging

from hotzenplotz.common import context


LOG = logging.getLogger(__name__)


def pipeline_factory(loader, global_config, **local_config):
    """Create a paste pipeline based on 'auth_strategy'"""
    pipeline = local_config[cfg.CONF.auth_strategy]
    pipeline = pipeline.split()
    filters = [loader.get_filter(n) for n in pipeline[:-1]]
    app = loader.get_app(pipeline[-1])
    filters.reverse()  # apply in reverse order!
    for filter in filters:
        app = filter(app)
    return app


class KeystoneContext(wsgi.Middleware):
    """Make a request context from keystone headers."""

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(app):
            return cls(app, **local_config)
        return _factory

    @webob.dec.wsgify
    def __call__(self, req):
        # Determine the user ID
        user_id = req.headers.get('X_USER_ID', req.headers.get('X_USER'))
        if not user_id:
            LOG.debug("Neither X_USER_ID nor X_USER found in request")
            return webob.exc.HTTPUnauthorized()

        # Determine the tenant
        project_id = req.headers.get('X_TENANT_ID', req.headers.get('X_TENANT'))

        # Suck out the roles
        roles = [r.strip() for r in req.headers.get('X_ROLE', '').split(',')]

        # Create a context with the authentication data
        ctx = context.Context(user_id, project_id, roles=roles)

        # Inject the context...
        req.environ['hotzenplotz.context'] = ctx

        return self.application
