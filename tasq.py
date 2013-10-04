#!/usr/bin/env python

"""
Enqueu task
"""

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013, SeongJae Park"
__license__ = "GPLv3"

import getpass
import os
import socket
import sys

USAGE = """
Usage: %s <enq|list> [command] [output file]
"""

HOST = "127.0.0.1"
PORT = 13537

DELIMETER = '_!@#_'

if __name__ == "__main__":
    if len(sys.argv) < 2 or (len(sys.argv) < 3 and sys.argv[1] != 'list'):
        print USAGE
        exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    user = getpass.getuser()
    path = os.getcwd()

    if sys.argv[1] == 'list':
        sock.sendall('list%s%s\n' % (DELIMETER, user))
        print sock.recv(1024)
        sock.close()
    elif sys.argv[1] == 'enq':
        cmd = ' '.join(sys.argv[2:-1])
        if cmd.find('_!@#_') != -1:
            print "command should not contain _!@#_"
            exit(1)
        output = sys.argv[-1]

        msg = "enq%s%s%s%s%s%s%s%s\n" % (DELIMETER, user, DELIMETER, path,
            DELIMETER, cmd, DELIMETER, output)

        sock.sendall(msg)
        sock.close()
