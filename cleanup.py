from argparse import ArgumentParser
from subprocess import check_call


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

    apps = ["rack", "server", "storage", "raid", "pdu"]
    parser = ArgumentParser(description="Clean up Juju environment")
    parser.add_argument("machines",
                        nargs="+",
                        type=int,
                        help="machines to remove")

    args = parser.parse_args()
    for m in args.machines:
        remove_machine(m)
    for a in apps:
        remove_application(a)

    print "Environment is clean."


if __name__ == "__main__":
    main()
