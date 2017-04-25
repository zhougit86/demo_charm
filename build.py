#!/usr/bin/python
import os
import shutil
from subprocess import check_call


def main():
    # clean up dist direction
    print 'removing dist/trusty'
    shutil.rmtree('./dist/trusty')

    # compile all
    for dirpath, subdirs, filenames in os.walk('.'):
        if dirpath.endswith('/charms'):
            for s in filter(lambda x: x.startswith('charm-'), subdirs):
                working_dir = os.path.join(dirpath, s)
                print "Charm build", working_dir
                check_call("cd %s && charm build" % working_dir, shell=True)


if __name__ == '__main__':
    main()
