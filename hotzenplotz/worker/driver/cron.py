import os
import datetime

from jinja2 import Environment,PackageLoader,TemplateNotFound
from hotzenplotz.openstack.common import cfg
from hotzenplotz.openstack.common import log as logging
from hotzenplotz.openstack.common import utils

from hotzenplotz.common import exception
from hotzenplotz.api import validator


LOG = logging.getLogger(__name__)

class CronHandler(object):

    """Handler Cron Resource
    """

    def __init__(self, **kwargs):
        env = Environment(loader=PackageLoader('hotzenplotz.worker','templates'))
        self.template =  env.get_template('cron')
        self.dir_path = None

   # @utils.synchronized('haproxy')
    def do_config(self, request):
        try:
            self._validate_request(request)
        except exception.BadRequest as e:
            LOG.warn('Bad request: %s' % e)
            raise exception.CronConfigureError(explanation=str(e))

        cmd = request['method']
        msg = request['cron_resource']

        if cmd == 'create_cron':
            try:
                self._create_cron(msg)
            except exception.CronCreateError as e:
                raise exception.CronConfigureError(explanation=str(e))

        elif cmd == 'delete_cron':
            try:
                self._delete_cron(msg)
            except exception.HaproxyDeleteError as e:
                raise exception.CronConfigureError(explanation=str(e))

        elif cmd == 'update_cron':
            try:
                self._update_cron(msg)
            except exception.CronUpdateError as e:
                raise exception.CronConfigureError(explanation=str(e))

    def _create_cron(self,msg,syntax_check=False):

        try:
            output = self.template.render(cron_resource=msg)
        except TemplateNotFound as e:
            raise TemplateNotFound(str(e))
        try:
            if not self.dir_path:
                self.dir_path = '/etc/puppet/modules/cron/'
            cron_name = msg['title']
            file_path = self.dir_path + cron_name 
            if not path.exists(file_path):
                 with open(file_path,'a') as f:
                    f.write(output)
        except exception.CronCreateError as e:
            raise exception.CronCreateError(explanation=str(e))
        if syntax_check:
            try:
                self._test_syntax(file_path)
            except exception.ProcessExecutionError as e:
                raise exception.CronCreateError(explanation=str(e))

        LOG.debug("Created the new cron successfully")

    def _delete_cron(self, msg):
        LOG.debug("Deleting cron  for NAME:%s USER: %s PROJECT:%s" %
                  (msg['id'], msg['user_id'], msg['project_id']))
        try:
            new_cfg_path = self._create_lb_deleted_haproxy_cfg(msg)
        except exception.HaproxyLBNotExists as e:
            LOG.warn('%s', e)
            return
            ##raise exception.HaproxyDeleteError(explanation=str(e))

        try:
            self._test_haproxy_config(new_cfg_path)
        except exception.ProcessExecutionError as e:
            raise exception.HaproxyDeleteError(explanation=str(e))

        rc, backup_path = self._backup_original_cfg()
        if rc != 0:
            raise exception.HaproxyDeleteError(explanation=backup_path)

        rc, strerror = self._replace_original_cfg_with_new(new_cfg_path)
        if rc != 0:
            raise exception.HaproxyDeleteError(explanation=strerror)

        if self._reload_haproxy_cfg(backup_path) != 0:
            e = 'Failed to reload haproxy'
            raise exception.HaproxyDeleteError(explanation=str(e))

        LOG.debug("Deleted the new load balancer successfully")

    def _update_cron(self, msg):
        LOG.debug("Updating the haproxy load "
                  "balancer for NAME:%s USER: %s PROJECT:%s" %
                  (msg['uuid'], msg['user_id'], msg['project_id']))

        try:
            lb_deleted_cfg_path = self._create_lb_deleted_haproxy_cfg(msg)
        except exception.HaproxyLBNotExists as e:
            LOG.warn('%s', e)
            raise exception.HaproxyUpdateError(explanation=str(e))

        try:
            new_cfg_path = self._create_lb_haproxy_cfg(
                msg, base_cfg_path=lb_deleted_cfg_path)
        except exception.HaproxyCreateCfgError as e:
            raise exception.HaproxyUpdateError(explanation=str(e))

        try:
            self._test_haproxy_config(new_cfg_path)
        except exception.ProcessExecutionError as e:
            raise exception.HaproxyUpdateError(explanation=str(e))

        LOG.debug("Updated the new load balancer successfully")

    def _validate_request(self, request):
        validate.check_tcp_request(request)

    def _get_lb_name(self, msg):
        # TODO(wenjianhn): utf-8 support, base64
        ##return "%s_%s" % (msg['project_id'],
        return "%s" % msg['uuid']



    def _is_lb_in_use(self, lb_name,
                      base_cfg_path='/etc/haproxy/haproxy.cfg'):
        with open(base_cfg_path) as cfg:
            lines = cfg.readlines()

        try:
            in_use_lb_name = [line.split()[1] for line in lines
                              if line.startswith('listen')]
        except IndexError:
            LOG.error("No item was found after listen directive,"
                      "is the haproxy configuraion file valid?")
            raise

        return lb_name in in_use_lb_name


    def _test_syntax(self, cfile_path):
        LOG.info('Testing the new puppet configuration file')
        cmd = "puppet parser validate %s" % cfile_path

        try:
            utils.execute(cmd)
        except exception.ProcessExecutionError as e:
            LOG.warn('Did not pass the configuration syntax test: %s', e)
            raise

    def _get_one_lb_info(self, line_all, line_index, line_total):
        value = []

        for i in range(line_index, line_total):
            line = line_all[i]

            if line.startswith('\t'):
                value.append(line)
            elif line.startswith('listen'):
                return i, value

        return line_total - 1, value

