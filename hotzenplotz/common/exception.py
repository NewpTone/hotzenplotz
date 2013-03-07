# Copyright 2013 XXXX Corporation
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
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Hotzenplotz base exception handling.
"""

from hotzenplotz.openstack.common import exception


class HotzenplotzException(exception.OpenstackException):
    """Base Hotzenplotz Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = _("An unknown exception occurred.")


class Unauthorized(HotzenplotzException):
    """
    HTTP 401 - Unauthorized: bad credentials.
    """
    message = _("Unauthorized: bad credentials.")


class Forbidden(HotzenplotzException):
    """
    HTTP 403 - Forbidden: your credentials don't give you access to this
    resource.
    """
    message = _("Forbidden: your credentials don't give you "
                "access to this resource")


class EndpointNotFound(HotzenplotzException):
    message = _("endpoint not found")


class AmbiguousEndpoints(HotzenplotzException):
    message = _("ambigous endpoint were found")


# api exceptions
class MissingParameter(HotzenplotzException):
    message = _("missing parameter: %(key)s.")


class InvalidParameter(HotzenplotzException):
    message = _("invalid parameter: %(msg)s.")


class CreateCronFailed(HotzenplotzException):
    message = _("create cron failed: %(msg)s")


class DeleteCronFailed(HotzenplotzException):
    message = _("delete cron failed: %(msg)s")


class UpdateCronFailed(HotzenplotzException):
    message = _("update cron failed: %(msg)s")


class GetCronFailed(HotzenplotzException):
    message = _("get cron failed: %(msg)s")


class GetAllCronFailed(HotzenplotzException):
    message = _("get all cron failed: %(msg)s")


class GetAllHttpServersFailed(HotzenplotzException):
    message = _("get all http servers failed: %(msg)s")


class CreateForInstanceFailed(HotzenplotzException):
    message = _("create cron for instance failed: %(msg)s")


class DeleteForInstanceFailed(HotzenplotzException):
    message = _("delete cron for instance failed: %(msg)s")


# db exceptions
class CronNotFound(HotzenplotzException):
    message = _("Cron %(load_balancer_id)s could not be found.")


class CronNotFoundByUUID(HotzenplotzException):
    message = _("Cron %(uuid)s could not be found by uuid.")


class CronNotFoundByTitle(HotzenplotzException):
    message = _("Cron %(cron_title)s could not be "
                "found by name.")


class CronNotFoundByInstanceUUID(HotzenplotzException):
    message = _("Cron %(instance_uuid)s could not be found by name.")


class CronConfigNotFound(HotzenplotzException):
    message = _("CronConfig %(config_id)s could not be found.")


class CronConfigNotFoundByCronId(HotzenplotzException):
    message = _("CronConfig %(load_balancer_id)s could not be found.")


class CronDomainNotFound(HotzenplotzException):
    message = _("CronDomain %(domain_id)s could not be found.")


class CronDomainNotFoundByName(HotzenplotzException):
    message = _("CronDomain %(domain_name)s could not be found.")


class CronInstanceAssociationNotFound(HotzenplotzException):
    message = _("CronInstanceAssociation %(load_balancer_id)s "
                "with %(instance_uuid)s could not be found")


class CommandError(Exception):
    pass


class ProcessExecutionError(IOError):
    def __init__(self, exit_code=None, output=None, cmd=None):
        self.exit_code = exit_code
        self.output = output
        self.cmd = cmd

        message = _('Command: %(cmd)s\n'
                    'Exit code: %(exit_code)s\n'
                    'Output: %(output)s\r\n') % locals()

        IOError.__init__(self, message)


class LBWorkerException(Exception):
    """Base Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = _("An unknown exception occurred.")

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.message % kwargs

            except Exception as e:
                # at least get the core message out if something happened
                message = self.message

        super(LBWorkerException, self).__init__(message)


class NotFound(LBWorkerException):
    message = _("Resource could not be found.")
    code = 404


class FileNotFound(NotFound):
    message = _("File %(file_path)s could not be found.")


class DirNotFound(NotFound):
    message = _("Directory %(dir)s could not be found.")


class ConfigNotFound(NotFound):
    message = _("Could not find config at %(path)s")


class Invalid(LBWorkerException):
    message = _("Unacceptable parameters.")
    code = 400


class InvalidType(Invalid):
    message = _("Valid type should be %(valid_type)s not %(invalid_type)s")


class InvalidPort(Invalid):
    message = _("Invalid port %(port)s. %(msg)s")


class InvalidIpv4Address(Invalid):
    message = _("%(address)s is not a valid IP v4 address.")


class NginxConfFileExists(Invalid):
    message = _("The supplied nginx configuration file (%(path)s) "
                "already exists, it is expected not to exist.")


class BadRequest(LBWorkerException):
    """
    The worker could not comply with the request since
    it is either malformed or otherwise incorrect.
    """
    message = _("%(explanation)s")


class ConfigureError(LBWorkerException):
    message = _("Could not configure the server.")


class NginxConfigureError(ConfigureError):
    message = _("Could not configure nginx: %(explanation)s")


class NginxCreateProxyError(NginxConfigureError):
    message = _("Could not create the nginx proxy: %(explanation)s")


class NginxUpdateProxyError(NginxConfigureError):
    message = _("Could not update the nginx proxy: %(explanation)s")


class NginxDeleteProxyError(NginxConfigureError):
    message = _("Could not delete the nginx proxy: %(explanation)s")


class HaproxyConfigureError(ConfigureError):
    message = _("Could not configure haproxy: %(explanation)s")


class HaproxyCreateError(HaproxyConfigureError):
    message = _("Could not create the haproxy proxy: %(explanation)s")


class HaproxyCreateCfgError(HaproxyConfigureError):
    message = _("Could not create the haproxy proxy "
                " configuration: %(explanation)s")


class HaproxyUpdateError(HaproxyConfigureError):
    message = _("Could not update the haproxy proxy: %(explanation)s")


class HaproxyDeleteError(HaproxyConfigureError):
    message = "Could not delete the haproxy proxy: %(explanation)s"


class HaproxyLBExists(Invalid):
    message = _("The supplied cron (%(name)s) "
                "already exists, it is expected not to exist.")


class HaproxyLBNotExists(Invalid):
    message = _("The supplied cron (%(name)s) "
                "does not exists, it is expected to exist.")
