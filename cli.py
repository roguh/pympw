# coding: utf-8
# TODO warn only v3 is implemented
import sys
import argparse
import threading
import time
import os
import getpass

import pyperclip

import master_password


default_counter = 1
default_type = 'Long'
help_cmds = ['?', 'help']
quit_cmds = ['quit']


def main():
    # TODO DOC
    parser = argparse.ArgumentParser(
        description='Passwords are generated locally, your master password is not sent to any server. http://masterpassword.app')
    parser.add_argument('--name', '-n', type=str,
                        default=None, help='your full name')
    parser.add_argument('--site', '-s', type=str, default=None,
                        help='site name (e.g. linux.org). omit this argument to start an interactive session.')
    parser.add_argument('--counter', '-c', type=int, default=default_counter,
                        help='positive integer less than 2**31=TODO')
    parser.add_argument('--type', type=str, default=default_type,
                        choices=master_password.template_classes.keys(), help='password type')
    parser.add_argument('--copy', '-y', action='store_true',
                        help='copy password to clipboard instead of printing it')
    parser.add_argument('--splitby', '-b', type=str, default=None,
                        help="more efficient interactive session. suggested values: tab, space, or '/'")
    parser.add_argument('--exit-after', '-e', type=int,
                        default=None, help='close script after this many seconds')

    # read site, counter, and type until quit
    args = parser.parse_args(sys.argv[1:])

    # TODO DOC
    try:
        if args.name is None:
            args.name = input('please type your full name > ')
        master_pw = getpass.getpass(
            'please type your master password > ')
    except (EOFError, KeyboardInterrupt, ValueError) as e:
        sys.exit(1)

    # precompute master key
    # TODO DOC
    key = master_password.master_key(args.name, master_pw)

    # print site password
    # TODO DOC
    if not args.site is None:
        print('site={}, type={}, counter={}'.format(
            args.site, args.type, args.counter))
        print(master_password.site_password(
            args.site, key, args.type, args.counter))

    # loop if no site
    # TODO DOC
    else:

        p = None
        e = threading.Event()
        # TODO DOC
        # start a thread that periodically checks for graceful exit
        # also start a countdown; when reached exit program
        if not args.exit_after is None:
            def start(exit_after):
                interval = 1 / 10
                for i in range(round(exit_after / interval)):
                    # TODO DOC
                    # Stop in case of early termination
                    if e.isSet():
                        return
                    time.sleep(interval)
                # TODO more graceful exit
                os._exit(0)
            p = threading.Thread(target=start, args=(args.exit_after,))
            p.start()

        def get(name, default):
            x = input('please type {}{} > '.format(name, ''  if default == '' 
                      else 'or ENTER for default={}'.format(default)))
            if x.lower() in help_cmds:
                parser.print_help()
                return default
            if x.lower() in quit_cmds:
                # TODO nicer
                raise EOFError 
            return x if x != '' else default
        try:
            # TODO DOC
            sb = args.splitby
            while True:
                if not sb is None and len(sb) > 0 and not sb in ['\n']:
                    ins = input('please type site name[{}type[{}counter]] > '.format(sb, sb))
                    # TODO DOC
                    if ins in help_cmds:
                        parser.print_help()
                        ins = ''
                    if ins in quit_cmds:
                        break
                    # TODO DOC
                    ins = ins.split(sb)
                    site = ins[0] if len(ins) > 0 else ''
                    _type = ins[1] if len(ins) > 1 else args.type
                    counter = ins[2] if len(ins) > 2 else args.counter
                else:
                    # TODO DOC
                    site = get('site name', '')
                    counter = get('counter', args.counter)
                    _type = get('type', args.type)

                # TODO DOC
                if site == '':
                    print('please enter a valid site name')
                    continue
                counter = int(counter)

                # print site password
                password = master_password.site_password(site, key, _type, counter)

                # TODO DOC
                if args.copy:
                    pyperclip.copy(password)
                    print('password copied to clipboard')
                else:
                    print(password)
        except (EOFError, KeyboardInterrupt, ValueError):
            print('\nbye')
            if not p is None:
                e.set()
                p.join()


if __name__ == '__main__':
    main()
