import os
import yaml
import subprocess

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import (
    status_set,
    open_port,
    config,
    log,
)
from charmhelpers.contrib.python.packages import pip_install,pip_install_requirements
from charmhelpers.core.templating import render
from charmhelpers.core.host import (
    adduser,
    service_restart,
    service_running,
    service_start,
)

# from charmhelpers.contrib.network.ip import (
#     get_iface_addr
# )


from charmhelpers.fetch import (
    apt_install,
    install_remote,
)

from charms import django
from charms.reactive import (
    hook,
    when,
    when_not,
    is_state,
    set_state,
    remove_state,
)
import time

djg_cfg = hookenv.config()         #load the cfg file

@hook('install')       # this hook makes the charm to execute in certain sequence. install->config-changed->start
def install():
    status_set('maintenance', 'changing the IP address of the ens9 to 2')
    subprocess.check_call(["ifconfig", "ens9", '2.2.2.2', 'netmask', '255.255.255.0'])
    time.sleep(5)

@hook('config-changed')
def change_config():
    status_set('maintenance', 'changing the IP address of the ens9 to 1')
    subprocess.check_call(["ifconfig", "ens9", '1.1.1.1', 'netmask', '255.255.255.0'])
    time.sleep(5)

@hook('start')
def start():
    status_set('maintenance', 'in the start status')
    subprocess.check_call(["ifconfig", "ens9", '3.3.3.3', 'netmask', '255.255.255.0'])
    time.sleep(5)


# @hook('bottom-relation-joined')
@when('bottom.available')
def add_bottom():
    status_set('active', 'bottom-added-changing the IP address of the ens9 to 4')
    subprocess.check_call(["ifconfig", "ens9", '4.4.4.4', 'netmask', '255.255.255.0'])
    time.sleep(5)

@hook('bottom-relation-joined')
def add_bottom_j():
    status_set('active', 'bottom-added-changing the IP address of the ens9 to 5')
    subprocess.check_call(["ifconfig", "ens9", '5.5.5.5', 'netmask', '255.255.255.0'])
    time.sleep(5)

@hook('bottom-relation-changed')
def add_bottom_c():
    status_set('active', 'bottom-added-changing the IP address of the ens9 to 6')
    subprocess.check_call(["ifconfig", "ens9", '6.6.6.6', 'netmask', '255.255.255.0'])
    time.sleep(5)


# @when_not('change the address to 2')
# def install():
#     # Do your setup here.
#     #
#     # If your charm has other dependencies before it can install,
#     # add those as @when() clauses above., or as additional @when()
#     # decorated handlers below
#     #
#     # See the following for information about reactive charms:
#     #
#     #  * https://jujucharms.com/docs/devel/developer-getting-started
#     #  * https://github.com/juju-solutions/layer-basic#overview
#     #
#     pip_install('time')
#     status_set('maintenance', 'changing the IP address of the ens9 to 2')     #show in the juju status
#
#     # apt_install(['build-essential', 'binutils-doc', 'autoconf', 'authbind',
#     #              'bison', 'libjpeg-dev', 'libfreetype6-dev', 'zlib1g-dev',
#     #              'libzmq3-dev', 'libgdbm-dev', 'libncurses5-dev', 'automake',
#     #              'libtool', 'libffi-dev', 'curl', 'git', 'gettext', 'flex',
#     #              'postgresql-client', 'postgresql-client-common', 'python3',
#     #              'python3-pip', 'python-dev', 'python3-dev', 'python-pip',
#     #              'libxml2-dev', 'virtualenvwrapper', 'libxslt-dev', 'git-core',
#     #              'python-git', 'libpq-dev','vim'])
#     #
#     # for pkg in ['django','gunicorn','circus','netifaces','netaddr',]:
#     #     pip_install(pkg)
#
#     # origin_ip = get_iface_addr("ens9")
#     # new_ip = origin_ip[0]+'1'
#
#     # source_install()
#     subprocess.check_call(["ifconfig","ens9", '2.2.2.2','netmask','255.255.255.0'])
#     time.sleep(5)
#     remove_state('change the address to 3')
#     set_state('change the address to 2')
#     # log(djg_cfg['django-port'])
#
# @when('change the address to 2')
# def change_3():
#     status_set('maintenance', 'changing the IP address of the ens9 to 3')
#     time.sleep(5)
#     subprocess.check_call(["ifconfig", "ens9", '3.3.3.3', 'netmask', '255.255.255.0'])
#     set_state('change the address to 3')
#
# @when('change the address to 3')
# def change_1():
#     status_set('maintenance', 'changing the IP address of the ens9 to 1')
#     time.sleep(5)
#     subprocess.check_call(["ifconfig", "ens9", '1.1.1.1', 'netmask', '255.255.255.0'])
#     remove_state('change the address to 2')
#
#
# def source_install():
#     source = djg_cfg.get('source', '')
#     status_set('maintenance', 'installing %s repo' % source)
#     if not os.path.exists(djg_cfg.get('install-path')):
#         os.makedirs(djg_cfg.get('install-path'))
#         os.chdir(djg_cfg.get('install-path'))



    # subprocess.check_call(["git","clone", source])
    #
    # dcfg.set('source-path', source_path)
    #
    # status_set('maintenance', 'installing project deps')
    # if dcfg.get('pip-requirements'):
    #     django.call([django.pip(), 'install', '-r',
    #                  dcfg.get('pip-requirements')])
    #
    # render(source='circus.ini.j2',
    #        target='/etc/circus.ini',
    #        owner='root',
    #        group='root',
    #        perms=0o644,
    #        context={
    #         'install_path': source_path,
    #         'wsgi': dcfg.get('wsgi'),
    #         'port': config('django-port'),
    #         'config_import': dcfg.get('config-import'),
    #     })
    #
    # render(source='circus.conf.j2',
    #        target='/etc/init/circus.conf',
    #        owner='root',
    #        group='root',
    #        perms=0o644,
    #        context={})
    #
    # set_state('django.source.available')
    # set_state('django.restart')



def touch(path):
    with open(path, 'a'):
        os.utime(path, None)
