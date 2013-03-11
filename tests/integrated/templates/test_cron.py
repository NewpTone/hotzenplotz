import hotzenplotz

from jinja2 import Environment,PackageLoader

env = Environment(loader=PackageLoader('hotzenplotz.worker','templates'))
template =  env.get_template('cron')

cron_resource = { 
    'title': 'git_daily_update',
    'command': 'git pull --all',
    'ensure': 'present',
    'hour': '12',
    'minute': '30',
    'user': 'root',
    }

