# import yaml
import subprocess

# from charmhelpers.core.unitdata import kv
from charmhelpers.core.hookenv import status_set
from charmhelpers.core import hookenv


djg_cfg = hookenv.config()



def manage(cmd):
    # dcfg = config()
    if not isinstance(cmd, list):
        cmd = cmd.split(' ')

    exe = [python(), 'manage.py']


    extra = []
    if djg_cfg.get('config-import'):
        extra.append('--settings=%s' % djg_cfg.get('config-import'))

    status_set('maintenance', ' '.join(['manage.py'] + cmd))
    call(exe + cmd + extra)

def call(cmd):
    # dcfg = config()
    subprocess.check_call(cmd, cwd=djg_cfg.get('source-path'))


def pip():
    return djg_cfg.get('pip', '/usr/bin/pip')


def python():
    return djg_cfg.get('python', '/usr/bin/python')
