from argparse import ArgumentParser
from pprint import pprint
from subprocess import check_call
from time import sleep

import yaml


def remove_machine(m):
    """Remove machines using juju remove-machine --force
    """
    args = "~/juju remove-machine %d --force" % m
    print args
    try:
        check_call(args, shell=False)
    except:
        pass


def remove_application(a):
    """Remove applications from juju env
    """
    args = "~/juju remove-application %s" % a
    print args
    try:
        check_call(args, shell=True)
    except:
        pass


def main():
    """Helper script to clean up Juju environment.

          Example:
            $ python cleanup.py 12 13 14

          will remove machine id 12-14, and remove applications
          hardcoded: rack, server, storage, raid, pdu....
    """

    bundle = yaml.load(open('bundle.yaml', 'r').read())
    apps = bundle['services'].keys()

    parser = ArgumentParser(description="Clean up Juju environment")
    parser.add_argument("machines",
                        nargs="+",
                        type=int,
                        help="machines to remove")

    args = parser.parse_args()
    start_at = args.machines[0]
    for a in apps:
        remove_application(a)
        sleep(2)

    for m in [start_at + i for i in range(len(bundle['machines']))]:
        remove_machine(m)
        sleep(3)
    for a in apps:
        remove_application(a)
        sleep(2)

    print "Environment is clean."


if __name__ == "__main__":
    main()
