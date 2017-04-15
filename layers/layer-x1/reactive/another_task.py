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
myproc = None


@when('state.2')
def state_3():
    """State 3
    """

    # Set status
    t = time.ctime(time.time())
    status_set('maintenance', 'state.3 %s' % t)

    # Workload
    log('state 3: Popen apt upgrade -------------')
    repo = "https://github.com/facebook/react.git"
    args = "git clone " + repo
    log(args)

    dest = os.path.join(os.getcwd(), 'react')
    if not os.path.exists(dest):
        global myproc
        myproc = subprocess.Popen(shlex.split(args), shell=False)

    # Next ->
    remove_state('state.2')
    set_state('state.0')
    set_state('test: blocking wait')


@when('test: blocking wait')
def test_blocking_wait():
    """Test blocking wait
    """

    func_name = sys._getframe().f_code.co_name

    # Set status
    t = time.ctime(time.time())
    status_set('maintenance', '%s %s' % (func_name, t))

    # Workload
    log('test: blocking wait -------------')
    global myproc
    if myproc:
        output, err = myproc.communicate()
        log('Proc output: %s' % output)
        log('Proc err: %s' % err)
    else:
        log('myproc is None')

    # Next ->
    remove_state('test: blocking wait')
