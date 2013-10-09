#!/usr/bin/env python

"""
Receive user's request and do things FIFO order.
"""
__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013, SeongJae Park"
__license__ = "GPLv3"

import os
import socket
import subprocess
import threading
import time

LOGFILE_PATH = "/home/cudata/tasq_log"
LOGFILE = None

TIMEOUT = 300

HOST = ''
PORT = 13537

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

conn = None

tasks = []

def do_log(log):
    with open(LOGFILE_PATH, 'a') as logf:
        logf.write("[%s] %s\n" % (time.strftime("%Y.%m.%d_%H:%M:%s"), log))

def accept_socket():
    global conn
    while True:
        s.listen(1)
        conn, addr = s.accept()
        print addr
        do_log("Connected by : %s" % addr.__str__())
        receive_msg()

process = None
def process_task():
    os.chdir(tasks[0]["path"])

    cmd = ('su %s -c "%s > %s 2>&1"' %
                (tasks[0]["user"], tasks[0]["job"], tasks[0]["out"]))
    def real_worker(cmd):
        global process
        process = subprocess.Popen(cmd, shell=True)
        process.communicate()

    thread = threading.Thread(target=real_worker, args=(cmd,))
    thread.start()

    thread.join(TIMEOUT)
    if thread.is_alive():
        do_log("timeout!")
        process.terminate()
        thread.join()

        os.system('echo "[tasq] Stop the command because ' +
                'it is running over %d seconds" >> %s' %
                (TIMEOUT, tasks[0]["out"]))

    del tasks[0]

def enq_task(task):
    alreadyqueued = len([t for t in tasks if t["user"] == task["user"]])
    if alreadyqueued >= 3:
        return False
    tasks.append(task)
    return True

def parse_msg(msg):
    """
    msg can be [enq | list] [user] [path] [job] [output]
    """
    splt = msg.split("_!@#_")
    task = {}
    task["cmd"] = splt[0]
    task["user"] = splt[1]
    if len(splt) > 2:
        task["path"] = splt[2]
        task["job"] = splt[3]
        task["out"] = splt[4]
    return task

def list_tasks(username):
    ret = "Queue State: "
    for task in tasks:
        if task["user"] == username:
            ret = ret + "\n\t%s" % task["job"]
        else:
            ret = ret + "\n\tOthers Job"
    return ret

def receive_msg():
    global conn
    received = ""
    while True:
        if not conn:
            time.sleep(5)
            continue
        try:
            received = received + conn.recv(1024)
        except:
            do_log("exception occurred while receive data.")
            continue
        if received:
            if received[-1] != '\n' and len(received) < 1024:
                continue
            do_log("received: %s" % received)
            task = parse_msg(received[:-1])
            do_log("parsed task: " % task)
            if task["cmd"] == 'list':
                conn.sendall(list_tasks(task["user"]))
            elif task["cmd"] == 'enq':
                if not enq_task(task):
                    conn.sendall("You already queued 3 tasks.")
                    do_log("reject enq reqeust. it already queued 3 tasks")
            conn.close()
            conn = None
            break

if __name__ == "__main__":
    threading._start_new_thread(accept_socket, ())

    while True:
        if len(tasks) > 0:
            process_task()
        else:
            time.sleep(5)
