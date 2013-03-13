# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
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

"""Method function """
from hotzenplotz import db
from hotzenplotz.common import exception
#from hotzenplotz.common import flags
#from hotzenplotz.common import utils
#from hotzenplotz.server import protocol
#from hotzenplotz.server import state
#from hotzenplotz.openstack.common.notifier import api as notifier
from hotzenplotz.openstack.common import log as logging

#FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)

#Cron
def get_all_crons(context, **kwargs):
   # expect_keys = [
   #     'user_id', 'project_id', 'all_tenants',
   # ]
   # utils.check_input_parameters(expect_keys, **kwargs)

    result = []
    try:
        all_tenants = int(kwargs['all_tenants'])
        if context.is_admin and all_tenants:
            filters = {}
        else:
            filters = {'project_id': kwargs['project_id']}
            context = context.elevated(read_deleted='no')
        all_crons = db.crons_get_all(context, filters=filters)
        for cron_ref in all_crons:
            cron_dict = {}
            cron_dict['cron_resource'] = cron_ref.to_dict()
            result.append(cron_dict)
    except Exception, exp:
        raise exception.GetAllCronFailed(msg=str(exp))

    return result

def get_cron(context, **kwargs):
#    expect_keys = [
#        'project_id', 'id',
#    ]
#    utils.check_input_parameters(expect_keys, **kwargs)

    result = None
    id = kwargs['id']
    try:
        cron_ref = db.cron_get_by_id(context, id)
        result = cron_ref.to_dict()
    except Exception, exp:
        raise exception.GetCronFailed(msg=str(exp))

    return {'cron_resource': result}


#Exec
def get_all_execs(context, **kwargs):
   # expect_keys = [
   #     'user_id', 'project_id', 'all_tenants',
   # ]
   # utils.check_input_parameters(expect_keys, **kwargs)

    result = []
    try:
        all_tenants = int(kwargs['all_tenants'])
        if context.is_admin and all_tenants:
            filters = {}
        else:
            filters = {'project_id': kwargs['project_id']}
            context = context.elevated(read_deleted='no')
        all_execs = db.execs_get_all(context, filters=filters)
        for exec_ref in all_execs:
            exec_dict = {}
            exec_dict['exec_resource'] = exec_ref.to_dict()
            result.append(exec_dict)
    except Exception, exp:
        raise exception.GetAllexecFailed(msg=str(exp))

    return result


def get_exec(context, **kwargs):

    result = None
    id = kwargs['id']
    try:
        exec_ref = db.exec_get_by_id(context, id)
        result = exec_ref.to_dict()
    except Exception, exp:
        raise exception.GetexecFailed(msg=str(exp))

    return {'exec_resource': result}

#File 
def get_all_files(context, **kwargs):
   # expect_keys = [
   #     'user_id', 'project_id', 'all_tenants',
   # ]
   # utils.check_input_parameters(expect_keys, **kwargs)

    result = []
    try:
        all_tenants = int(kwargs['all_tenants'])
        if context.is_admin and all_tenants:
            filters = {}
        else:
            filters = {'project_id': kwargs['project_id']}
            context = context.elevated(read_deleted='no')
        all_files = db.files_get_all(context, filters=filters)
        for file_ref in all_files:
            file_dict = {}
            file_dict['file_resource'] = file_ref.to_dict()
            result.append(file_dict)
    except Exception, exp:
        raise exception.GetAllfileFailed(msg=str(exp))

    return result

def get_file(context, **kwargs):
#    expect_keys = [
#        'project_id', 'id',
#    ]
#    utils.check_input_parameters(expect_keys, **kwargs)

    result = None
    id = kwargs['id']
    try:
        file_ref = db.file_get_by_id(context, id)
        result = file_ref.to_dict()
    except Exception, exp:
        raise exception.GetfileFailed(msg=str(exp))

    return {'file_resource': result}


def get_all_groups(context, **kwargs):
   # expect_keys = [
   #     'user_id', 'project_id', 'all_tenants',
   # ]
   # utils.check_input_parameters(expect_keys, **kwargs)

    result = []
    try:
        all_tenants = int(kwargs['all_tenants'])
        if context.is_admin and all_tenants:
            filters = {}
        else:
            filters = {'project_id': kwargs['project_id']}
            context = context.elevated(read_deleted='no')
        all_groups = db.groups_get_all(context, filters=filters)
        for group_ref in all_groups:
            group_dict = {}
            group_dict['group_resource'] = group_ref.to_dict()
            result.append(group_dict)
    except Exception, exp:
        raise exception.GetAllgroupFailed(msg=str(exp))

    return result

def get_group(context, **kwargs):
#    expect_keys = [
#        'project_id', 'id',
#    ]
#    utils.check_input_parameters(expect_keys, **kwargs)

    result = None
    id = kwargs['id']
    try:
        group_ref = db.group_get_by_id(context, id)
        result = group_ref.to_dict()
    except Exception, exp:
        raise exception.GetgroupFailed(msg=str(exp))

    return {'group_resource': result}



def get_all_packages(context, **kwargs):
   # expect_keys = [
   #     'user_id', 'project_id', 'all_tenants',
   # ]
   # utils.check_input_parameters(expect_keys, **kwargs)

    result = []
    try:
        all_tenants = int(kwargs['all_tenants'])
        if context.is_admin and all_tenants:
            filters = {}
        else:
            filters = {'project_id': kwargs['project_id']}
            context = context.elevated(read_deleted='no')
        all_packages = db.packages_get_all(context, filters=filters)
        for package_ref in all_packages:
            package_dict = {}
            package_dict['package_resource'] = package_ref.to_dict()
            result.append(package_dict)
    except Exception, exp:
        raise exception.GetAllpackageFailed(msg=str(exp))

    return result

def get_package(context, **kwargs):
#    expect_keys = [
#        'project_id', 'id',
#    ]
#    utils.check_input_parameters(expect_keys, **kwargs)

    result = None
    id = kwargs['id']
    try:
        package_ref = db.package_get_by_id(context, id)
        result = package_ref.to_dict()
    except Exception, exp:
        raise exception.GetpackageFailed(msg=str(exp))

    return {'package_resource': result}



def get_all_services(context, **kwargs):
   # expect_keys = [
   #     'user_id', 'project_id', 'all_tenants',
   # ]
   # utils.check_input_parameters(expect_keys, **kwargs)

    result = []
    try:
        all_tenants = int(kwargs['all_tenants'])
        if context.is_admin and all_tenants:
            filters = {}
        else:
            filters = {'project_id': kwargs['project_id']}
            context = context.elevated(read_deleted='no')
        all_services = db.services_get_all(context, filters=filters)
        for service_ref in all_services:
            service_dict = {}
            service_dict['service_resource'] = service_ref.to_dict()
            result.append(service_dict)
    except Exception, exp:
        raise exception.GetAllserviceFailed(msg=str(exp))

    return result

def get_service(context, **kwargs):
#    expect_keys = [
#        'project_id', 'id',
#    ]
#    utils.check_input_parameters(expect_keys, **kwargs)

    result = None
    id = kwargs['id']
    try:
        service_ref = db.service_get_by_id(context, id)
        result = service_ref.to_dict()
    except Exception, exp:
        raise exception.GetserviceFailed(msg=str(exp))

    return {'service_resource': result}



def get_all_users(context, **kwargs):
   # expect_keys = [
   #     'user_id', 'project_id', 'all_tenants',
   # ]
   # utils.check_input_parameters(expect_keys, **kwargs)

    result = []
    try:
        all_tenants = int(kwargs['all_tenants'])
        if context.is_admin and all_tenants:
            filters = {}
        else:
            filters = {'project_id': kwargs['project_id']}
            context = context.elevated(read_deleted='no')
        all_users = db.users_get_all(context, filters=filters)
        for user_ref in all_users:
            user_dict = {}
            user_dict['user_resource'] = user_ref.to_dict()
            result.append(user_dict)
    except Exception, exp:
        raise exception.GetAlluserFailed(msg=str(exp))

    return result

def get_user(context, **kwargs):
#    expect_keys = [
#        'project_id', 'id',
#    ]
#    utils.check_input_parameters(expect_keys, **kwargs)

    result = None
    id = kwargs['id']
    try:
        user_ref = db.user_get_by_id(context, id)
        result = user_ref.to_dict()
    except Exception, exp:
        raise exception.GetuserFailed(msg=str(exp))

    return {'user_resource': result}
