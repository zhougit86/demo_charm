

import time

from charmhelpers.core.hookenv import (
    status_set,
    open_port,
    config,
    log,
)
from charms.reactive import (
    hook,
    when,
    when_not,
    is_state,
    set_state,
    remove_state,
)

from charmhelpers.core.templating import render
from charmhelpers.contrib.python.packages import pip_install
from charmhelpers.fetch.centos import install

from subprocess import check_call
@when_not('layer-centos.installed')
# @hook('install')
def install_layer_centos():
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    # install('python3')
    status_set('maintenance', 'changing the IP address of the ens9 to 2')

    # pip_install('django')
    # pip_install('python - jinja2')
    time.sleep(30)

    set_state('layer-centos.installed')

# @hook('config-changed')
@when('layer-centos.installed')
def change_config():
    test={'name':'lctc','age':123}
    render(source='vanilla_config.conf',
           target='/root/config.py',
           owner='root',
           perms=0o775,
           context={
               'object':test,
           })