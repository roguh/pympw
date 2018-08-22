# coding: utf-8
# TODO copy to clipboard
# TODO tab/space/slash separated site/type or site/type/counter

import sys
import argparse
import threading 
import time
import os

import mpw


default_counter = 1
default_type = 'Long'


def main():
    # TODO DOC
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--name', type=str, default=None, help='your full name')
    parser.add_argument('--site', type=str, default=None, help='site name (e.g. linux.org)')
    parser.add_argument('--counter', type=int, default=default_counter, help='positive integer less than 2**31=TODO')
    parser.add_argument('--type', type=str, default=default_type, choices=mpw.template_classes.keys(), help='password type')
    parser.add_argument('--copy', type=bool, default=False, help='copy password to clipboard instead of printing it')
    parser.add_argument('--exit-after', type=int, default=None, help='close script after this many seconds')

    # read site, counter, and type until quit
    args = parser.parse_args(sys.argv[1:])

    # TODO DOC
    try:
        if args.name is None:
            args.name = input('please type your full name > ')
        master_password = input('please type your master password > ')
    except (EOFError, KeyboardInterrupt, ValueError) as e:
        sys.exit(1)

    # precompute master key
    # TODO DOC
    key = mpw.master_key(args.name, master_password)

    # print site password
    # TODO DOC
    if not args.site is None:
        print('site={}, type={}, counter={}'.format(args.site, args.type, args.counter))
        print(mpw.site_password(args.site, key, args.type, args.counter)) 

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
            x = input('please type {} or ENTER for default={} > '.format(name, default))
            return x if x != '' else default
        try:
            # TODO DOC
            while True:
                site = input('site name > ')
                if site == '':
                    print('please enter a valid site name')
                    continue
                counter = get('counter', args.counter)
                counter = int(counter)
                _type = get('type', args.type)

                # print site password
                print(mpw.site_password(site, key, _type, counter)) 
        except (EOFError, KeyboardInterrupt, ValueError):
            print('\nbye')
            if not p is None:
                e.set()
                p.join()

if __name__ == '__main__':
    main()
