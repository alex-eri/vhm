#coding:utf-8
__author__ = 'eri'
import config
import argparse
import glob
import os
import sys
import pwd
import grp

gid = grp.getgrnam("www-data").gr_gid
uid = pwd.getpwnam("www-data").pw_uid

def iterhosts(fu):
    def inner(names):
        for name in names:
            fu(names)
    return inner

def error(s):
    print(s,file=sys.stderr)

@iterhosts
def new(name):
    conf = os.path.join(config.etcpath,config.enabledpath,name)
    docroot = os.path.join(config.hostspath,name)

    with open(conf,'w') as f:
        f.write(config.pattern.format(name=name,docroot=docroot))

    os.makedirs(docroot,mode=0o775)
    os.chown(docroot,uid,gid)

    with open('/etc/hosts','a') as h:
        h.write('\n#VirtualHost {name}\n127.0.1.1\t{name} www.name')


@iterhosts
def delete(name):
        print(name)

@iterhosts
def enable(name):
        print('enabled:')
        print(name)

@iterhosts
def disable(name):
        print('disabled:')
        print(name)


def list():
    print('enabled:')
    for name in glob.glob(os.path.join(config.etcpath,config.enabledpath)):
        print(name)
    else:
        print('none')
    print('available')
    for name in glob.glob(os.path.join(config.etcpath,config.availablepath)):
        print(name)
    else:
        print('none')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manages VirtualHosts.')
    parser.add_argument('--new', dest='process', action='append_const',
                   const=new,
                   help='add new virtual host')

    parser.add_argument('--delete', dest='process', action='append_const',
                   const=delete,
                   help='delete virtual host')

    parser.add_argument('--enable', dest='process', action='append_const',
                   const=enable,
                   help='enable virtual host')

    parser.add_argument('--disable', dest='process', action='append_const',
                   const=disable,
                   help='disable virtual host')

    parser.add_argument('--list', action='store_true', default=False,
                   help='disable virtual host')

    parser.add_argument('hosts', metavar='host', type=str, nargs='*',
                   help='hostname to process')

    args = parser.parse_args()
    if args.list:
        list()
    if args.hosts:
        if os.getuid():
            error('Need Root!')
            exit(1)
        for action in args.process:
            action(args.hosts)
