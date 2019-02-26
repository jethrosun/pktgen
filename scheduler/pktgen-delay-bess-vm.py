# -*- coding: utf-8 -*-

"""
pktgen_scheduler.py
---------
pktgen_scheduler talks with pktgen_servers, schedules
jobs and listens for statuses.
"""
import sys
import code
import json
import math
import time
import Queue
import socket
import struct
import logging
import argparse
import threading
import subprocess

from os import O_NONBLOCK, read
from fcntl import F_GETFL, F_SETFL, fcntl

import job_pb2
import paramiko
import status_pb2

from control import *


def connect_test_machine(machine='c3'):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(hostname=machine) # This assumes we don't need a key to ssh.
    return conn

def exec_command_and_wait(conn, cmd):
    i, o, e = conn.exec_command(cmd)
    o = list(o)
    e = list(e)
    return (o, e)
def exec_command_noblock(conn, cmd):
    i, o, e = conn.exec_command(cmd)
    # o.setblocking(0)
    return (o, e)
def add_server(q, server, port):
    key = "%s_%d"%(server, port)
    q.add_node(Node(key, server, port))
    return key

def run_flow(q, key):
    q.results_event.clear()
    q.add_job(key, Job(1, {
        "tx_rate": 10000,
        "duration": 24 * 60 * 60 * 1000,
        "warmup": 0,
        "num_flows": 1,
        "size_min": 64, "size_max": 64,
        "life_min": 60*1000, "life_max": 24*60*60*1000,
        "port_min": 80, "port_max": 80,
        "latency": False,
        "src_mac": "68:05:ca:00:00:ab",
        "dst_mac": "68:05:ca:00:00:01",
        "online": True}))

def stop_and_measure(q, key):
    q.add_job(key, Job(0, {"print": True, "stop": True}))
    q.results_event.wait()
    measure = q.results
    return measure

def restart_pktgen(handle, port, pcie):
    if handle:
        handle.kill()
        handle.wait()
    handle = subprocess.Popen(["stdbuf", \
                               "-o0", \
                               "-e0", \
                               "build/pktgen", \
                               "-c", "0xf0", \
                               "-w", str(pcie), \
                               "--", str(port)], \
                               stdout=subprocess.PIPE, \
                               stderr=subprocess.PIPE)
    flags = fcntl(handle.stdout, F_GETFL)
    fcntl(handle.stdout, F_SETFL, flags | O_NONBLOCK)
    flags = fcntl(handle.stderr, F_GETFL)
    fcntl(handle.stderr, F_SETFL, flags | O_NONBLOCK)
    while True:
        try:
            l = read(handle.stdout.fileno(), 1024)
            if l.startswith("Init core"):
                print "Detected pktgen up"
                return handle
        except OSError:
            if handle.poll() is not None:
                break
            continue
        # l = handle.stdout.readline()
        # l2 = handle.stderr.readline()

def output_data(handle):
    while True:
        try:
            l = read(handle.stdout.fileno(), 1024)
            print l
        except OSError:
            break
    while True:
        try:
            l = read(handle.stderr.fileno(), 1024)
            print l
        except OSError:
            break
def measure_delay(q, pgen_server, pgen_port, server, out):
    handle = None
    conn = connect_test_machine(server)
    key = add_server(q, pgen_server, pgen_port)
    measure_time = 15 # seconds
    start_container = "/opt/e2d2/scripts/start-bess-vm.sh start %d | tee /tmp/start"
    stop_container = "/opt/e2d2/scripts/start-bess-vm.sh stop"
    stop_container_hard = "/opt/e2d2/scripts/start-bess-vm.sh hardkill"
    o, e = exec_command_and_wait(conn, stop_container)
    for delay in xrange(0, 5000, 50):
        try:
            success = False
            while not success:
                print "Starting pgen"
                success = True
                handle = restart_pktgen(handle, pgen_port, "81:00.0")
                print "Starting VM"
                o,e = exec_command_noblock(conn, start_container%(delay))
                while True:
                    l = o.readline()
                    print l
                    if l.strip() == "Successfully started":
                        break
                    if l.strip() == "Fail Fail Fail":
                        print "Detected failure"
                        success = False
                        break
                if not success:
                    print "Stopping"
                    o,e = exec_command_noblock(conn, stop_container)
                    o,e = exec_command_noblock(conn, stop_container_hard)
                    print "Restarting"
                    continue
                print "VM started"
                run_flow(q, key)
                print "Measuring"
                time.sleep(measure_time)
                # output_data(handle)
                print "Stopping"
                m = stop_and_measure(q, key)
                rx_mpps_mean = 0
                tx_mpps_mean = 0
                for v in m.itervalues():
                    for measure in v.itervalues():
                        if measure['rx_mpps_mean'] > 0.0:
                            rx_mpps_mean += measure['rx_mpps_mean']
                            tx_mpps_mean += measure['tx_mpps_mean']
                o, e = exec_command_and_wait(conn, stop_container)
                print "Out ", '\n\t'.join(o)
                print "Err ", '\n\t'.join(e)
                if tx_mpps_mean < 1.0:
                    success = False
                    print "Restarting"
                else:
                    print delay, rx_mpps_mean, tx_mpps_mean
                    print >>out, delay, rx_mpps_mean, tx_mpps_mean
                    out.flush()
        except:
            print "Caught exception"
            o, e = exec_command_and_wait(conn, stop_container)
            print "Out ", '\n\t'.join(o)
            print "Err ", '\n\t'.join(e)
            raise

def main():
    q_ip = 'localhost'
    q_port = 1800
    q_nodes_file = q_jobs_file = None

    parser = argparse.ArgumentParser(
        description="pktgen_scheduler schedules jobs for pktgen_servers")

    q = Q(q_ip, q_port, q_nodes_file, q_jobs_file)
    q.start()
    try:
        measure_delay(q, "127.0.0.1", 5000, "c3", open(sys.argv[1], "w"))
    finally:
        q.stop()


if __name__ == '__main__':
    main()
