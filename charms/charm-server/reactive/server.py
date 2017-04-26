import os
import pprint
import pwd
import re
import shlex
import subprocess
import sys
import time

import yaml

from charmhelpers.contrib.python.packages import pip_install
from charmhelpers.contrib.python.packages import pip_install_requirements
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import config
from charmhelpers.core.hookenv import log
from charmhelpers.core.hookenv import open_port
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.host import adduser
from charmhelpers.core.host import service_restart
from charmhelpers.core.host import service_running
from charmhelpers.core.host import service_start
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_install
from charmhelpers.fetch import install_remote
from charms.reactive import hook
from charms.reactive import is_state
from charms.reactive import only_once
from charms.reactive import remove_state
from charms.reactive import set_state
from charms.reactive import when
from charms.reactive import when_not

hooks = hookenv.Hooks()
TEST_TIMEOUT = 1
myproc = None


@hook("install")
def install():
    """Set the installed state.

    This is the entry point.
    """

    # test: subprocess
    log("install-----------------")
    p = subprocess.Popen(args, shell=True)
    with open('/tmp/myserver.log', 'w') as f:
        f.write('install hook\n')

    # do sth
    config = hookenv.config()
    config['playbook'] = 'give me a name'


@hook('config-changed')
def config_changed():
    config = hookenv.config()

    log("I'm here---------------------")
    log('New IP: ' + config['server-ip'])
    if config.changed['server-ip']:
        log("Server IP changed: " + config['server-ip'])
    with open('/tmp/myserver.log', 'a') as f:
        f.write('new config: %s\n' % config)


@hook("start")
def start():
    pass


@only_once
def state_0():
    log('server start------------------')
    set_state('state.1')


@when('state.1')
def state_1():
    """State 1
    """

    # Set status
    remove_state("state.1")
    status_set('maintenance', 'server not configured')
