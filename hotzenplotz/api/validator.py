# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Sina Corporation
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

import netaddr

from hotzenplotz.openstack.common import uuidutils


def validate_uuid(data, valid_data=None):
    if not uuidutils.is_uuid_like(data):
        pass


def validate_ip_address(data, valid_data=None):
    try:
        netaddr.IPAddress(data)
    except Exception:
        pass


def validate_mac_address(data, valid_data=None):
    try:
        netaddr.EUI(data)
    except Exception:
        pass


def validate_server_name(data, valid_data=None):
    SERVER_NAME_PATTERN = ("(?=^.{1,254}$)(^(?:(?!\d+\.|-)[a-zA-Z0-9_\-]"
                           "{1,63}(?<!-)\.?)+(?:[a-zA-Z]{2,})$)")
    try:
        if re.match(data, SERVER_NAME_PATTERN):
            return
    except TypeError:
        pass
