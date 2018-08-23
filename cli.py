#!/usr/bin/env python3
# coding: utf-8
import sys
import argparse
from time import time as now
import getpass

import signal
import pyperclip
import subprocess
# import colorama # TODO

import master_password as mpw


default_counter = 1
default_type = 'long'
help_cmds = ['?', 'help']
quit_cmds = ['quit']


def main():
    parser = argparse.ArgumentParser(
        description='CLI to Master Password algorithm v3. Passwords are generated locally, your master password is not sent to any server. http://masterpassword.app')
    parser.add_argument('--name', '-n', type=str,
                        default=None, help='your full name')
    parser.add_argument('--site', '-s', type=str, default=None,
                        help='site name (e.g. linux.org). omit this argument to start an interactive session.')
    parser.add_argument('--counter', '-c', type=int, default=default_counter,
                        help='positive integer less than 2**31=4294967296')
    parser.add_argument('--type', type=str, default=default_type,
                        choices=mpw.template_class_names, help='password type')
    parser.add_argument('--copy', '-y', action='store_true',
                        help='copy password to clipboard instead of printing it')
    parser.add_argument('--hide-pw', '-d', action='store_true',
                        help='never print passwords')
    parser.add_argument('--splitby', '-b', type=str, default=None,
                        help="more efficient interactive session. suggested values: tab, space, or '/'")
    parser.add_argument('--exit-after', '-e', type=int,
                        default=None, help='script will timeout and close after this many seconds')
    parser.add_argument( "--exit-command", type=str, default=None, help="run this command if the script times out")
    parser.add_argument( "--keepalive", "-k", action="store_true", help="keep program from timing out by pressing ENTER")
    parser.add_argument( "--quiet", "-q", action="store_true", help="less output")

    # read site, counter, and type until quit
    args = parser.parse_args(sys.argv[1:])

    if args.hide_pw:
        args.copy = True

    def verbose_print(*_args, **kwargs):
        if not args.quiet:
            print(*_args, **kwargs)

    # read Name if not passed as argument
    # read password without echo
    courtesy = '' if args.quiet else 'please type your '
    try:
        verbose_print("Welcome to Master Password")
        if args.name is None:
            args.name = input(courtesy + 'full name > ')

        master_pw = getpass.getpass(courtesy + 'master password > ')
    except (EOFError, KeyboardInterrupt, ValueError) as e:
        sys.exit(1)

    # precompute master key
    key = mpw.master_key(args.name, master_pw)
    del master_pw
    del args.name

    # print site password if site name was passed as argument
    if not args.site is None:
        verbose_print('site={}, type={}, counter={}'.format(args.site, 
                      args.type, args.counter))
        print(mpw.site_password(args.site, key, args.type, args.counter))
        return

    # loop if no site name was given 
    if not args.exit_after is None:
        # start a chain of ALARM signals that periodically check if the program
        # must close now 
        handler_params = {
            "active": now(),
            "scheduled": now()
        }

        def handler(signum, frame):
            p = handler_params
            active, scheduled = p["active"], p["scheduled"]

            active_since = lambda t: now() - (1 + active) < t
            next_delay = max(1, round(active - scheduled))
            # print('ALARM!', now() - active, active_since(args.exit_after), active, next_delay, active - scheduled) 
            if not active_since(args.exit_after):
                raise InterruptedError
            else:
                p["scheduled"] = now()
                signal.alarm(next_delay)
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(args.exit_after)

    courtesy = '' if args.quiet else 'please type '

    def get_input(prompt):
        r = input(prompt)
        if args.keepalive:
            handler_params["active"] = now()
        return r

    def get_param(name, default):
        x = get_input(courtesy + name + (''  if default == '' else ' or ENTER for default=' + str(default)) + ' > ')
        if x.lower() in help_cmds:
            parser.print_help()
            return default
        if x.lower() in quit_cmds:
            quit = True 
        return x if x != '' else default
    try:
        # run a loop that asks for site name, template class (aka password
        # type, and counter
        sb = args.splitby
        quit = False
        password = None 
        while not quit:
            if not sb is None and len(sb) > 0 and not sb in ['\n']:
                ins = get_input(courtesy + 'site name[{}type[{}counter]] > '.format(sb, sb))
                # is this a request for help? 
                if ins in help_cmds:
                    parser.print_help()
                    ins = ''
                if ins in quit_cmds:
                    quit = True
                # split input by the given split-by character 
                ins = ins.split(sb)
                site = ins[0] if len(ins) > 0 else ''
                _type = ins[1] if len(ins) > 1 else args.type
                counter = ins[2] if len(ins) > 2 else args.counter
            else:
                # get site, counter, and password type, or defaults 
                site = get_param('site name', '')
                counter = get_param('site counter', args.counter)
                _type = get_param('site type', args.type)

            # nag until a non-empty site name is given 
            if site == '':
                verbose_print('please enter a valid site name')
                continue
            try:
                counter = int(counter)
                if counter < 1:
                    raise ValueError
            except ValueError:
                verbose_print("please enter a positive integer")
                continue

            password = mpw.site_password(site, key, _type, counter)

            # either print password or copy it to clipboard 
            if args.copy:
                pyperclip.copy(password)
                verbose_print('password copied to clipboard')
            if not args.hide_pw:
                print(password)
    except (EOFError, KeyboardInterrupt):
        pass
    except InterruptedError:
        # run command after timeout
        verbose_print(args.exit_after, 'second timeout reached')
        if not args.exit_command is None:
            subprocess.call(args.exit_command, shell=True)
    finally:
        print('bye')
        del key
        del password


if __name__ == '__main__':
    main()
