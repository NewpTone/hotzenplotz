import datetime
import unittest

from hotzenplotz.openstack.common import uuidutils
from hotzenplotz.common import config
from hotzenplotz.common import context
from hotzenplotz.common import exception
from hotzenplotz import db
from hotzenplotz.db.sqlalchemy import session


class DBApiTestCase(unittest.TestCase):

    def setUp(self):
        super(DBApiTestCase, self).setUp()
#        import pdb; pdb.set_trace()
        engine = session.get_engine()
        self.connection = engine.connect()
        #self.context = context.get_context()
        self.configs = dict()
        self.user_id = 'fake-user-0'
        self.project_id = 'fake-project-0'
        self.cron = {
            'id':        uuidutils.generate_uuid(),
            'user_id':   self.user_id,
            'project_id': self.project_id,
            'title':     'apt-mirror',
            'command':   'apt-mirror',
            'hour':      '21',
            'minute':    '30',
            'user':      'root',         
        }
        self.context = context.get_context(self.user_id, self.project_id)

    def tearDown(self):
        pass

    def truncate_table(self, table):
        execution = self.connection.execution_options(autocommit=True)
        execution.execute("TRUNCATE %s;" % table)

    def truncate_all_tables(self):
        self.truncate_table('crons')

    def compare_records(self, expect, actual, skiped=None):
        for k, v in actual.__dict__.iteritems():
            if k.startswith('_') or k in skiped:
                continue
            elif isinstance(v, datetime.datetime):
                continue
            self.assertEqual(expect[k], v)

    def test_table_create(self):
        self.truncate_all_tables()
        print "just a test"
        expect = db.cron_create(self.context, self.cron)
        actual = db.cron_get_by_id(self.context, expect.id)
        self.compare_records(expect, actual, skiped=['id'])


if __name__ == '__main__':
    unittest.main()
