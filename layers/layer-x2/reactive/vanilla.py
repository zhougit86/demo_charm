import os
import pprint
import pwd
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
from charms.reactive import remove_state
from charms.reactive import set_state
from charms.reactive import when
from charms.reactive import when_not

hooks = hookenv.Hooks()
TEST_TIMEOUT = 3


@when_not("x2")
def entry():
    set_state("x2")
    set_staus("x2 started")


@when('state.1')
def state_2():
    """State 2
    """
    time.sleep(TEST_TIMEOUT)
    set_state('state.2')
    t = time.ctime(time.time())
    status_set('active', 'state.2 %s' % t)


@when('state.2')
def state_3():
    """State 3
    """
    time.sleep(TEST_TIMEOUT)
    set_state('state.0')
    t = time.ctime(time.time())
    status_set('active', 'state.0 %s' % t)
