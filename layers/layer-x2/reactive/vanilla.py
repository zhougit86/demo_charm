import os
import pprint
import pwd
import re
import subprocess
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


@hooks.hook("install")
def install():
    """Set the installed state.

    This is the entry point.
    """

    # install everything needed to construct the environment
    pip_install('time')

    # this assertion should fail!
    assert config['app-name'] == 'x1'

    # test: subprocess
    args = [x.string() for x in "sudo apt update".split(" ")]
    p = subprocess.Popen(args, shell=True)

    # do sth
    config = hookenv.config()
    config['playbook'] = 'give me a name'


@hooks.hook('config-changed')
def config_changed():
    config = hookenv.config()

    tmp = pprint.pformat(config, indent=2)
    with open('/tmp/mylog.log', 'w') as f:
        f.write(tmp)

    assert 'give me' in config['playbook']
    status_set('maintenance', 'my config changed')


@hooks.hook("start")
def start():
    pass


@only_once
def state_0():
    log('x2------------------')
    status_set('maintenance', 'start: state.0')
    time.sleep(TEST_TIMEOUT)


@when('state.0')
def state_1():
    """State 1
    """

    # Set status
    t = time.ctime(time.time())
    status_set('maintenance', 'state.1 %s' % t)

    # Workload
    time.sleep(TEST_TIMEOUT)

    # Next ->
    remove_state('state.0')
    set_state('state.1')


@when('state.1')
def state_2():
    """State 2
    """

    # Set status
    t = time.ctime(time.time())
    status_set('maintenance', 'state.2 %s' % t)

    # Workload
    time.sleep(TEST_TIMEOUT)

    # Next ->
    remove_state('state.1')
    set_state('state.2')


@when('state.2')
def state_3():
    """State 3
    """

    # Set status
    t = time.ctime(time.time())
    status_set('maintenance', 'state.3 %s' % t)

    # Workload
    time.sleep(TEST_TIMEOUT)

    # Next ->
    remove_state('state.2')
    set_state('state.0')
