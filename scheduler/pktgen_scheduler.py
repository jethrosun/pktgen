# -*- coding: utf-8 -*-

"""
pktgen_scheduler.py
---------
pktgen_scheduler talks with pktgen_servers, schedules
jobs and listens for statuses.
"""
import sys
import math
import time
import argparse

from control import *


def demo(servers, q):
    """
    server = [(server_ip,server_port),...]
    """
    n = len(servers)
    try:
        for i, s in enumerate(servers):
            q.add_node(Node(str(i), s[0], s[1]))

        for i in range(n):
            q.add_job(str(i), Job(1, {
                "tx_rate": 100,
                "duration": 5000,
                "warmup": 1000,
                "num_flows": 1,
                "size_min": 768, "size_max": 768,
                "life_min": 5000, "life_max": 5000,
                "port_min": 80, "port_max": 80,
                "online": True}))
            time.sleep(5)
            q.add_job(str(i), Job(2, {
                "tx_rate": 100,
                "duration": 5000,
                "warmup": 1000,
                "num_flows": 2,
                "size_min": 768, "size_max": 768,
                "life_min": 5000, "life_max": 5000,
                "port_min": 443, "port_max": 443,
                "online": True}))
    except:
        for i in range(n):
            q.add_job(str(i), Job(0, {"stop": True}))

def increase_smoothly(q, server, start_rate, stop_rate, steps, duration, margin, end):
    diff = float(stop_rate - start_rate)
    step_size = math.ceil(diff/float(steps))
    duration_per_step = int(math.ceil(duration / float(steps)))
    runduration = int(math.ceil(duration_per_step + margin))
    for rate in xrange(int(start_rate), int(stop_rate) + 1, int(step_size)):
        q.add_job(server, Job(1, {\
            "tx_rate": rate,\
            "duration": runduration * 1000,\
            "warmup": 0,\
            "num_flows": 300,\
            "size_min": 768,\
            "size_max": 768,\
            "life_min": 1,\
            "life_max": 120,\
            "online": True\
            }))
        time.sleep(duration_per_step)
    q.add_job(server, Job(1, {\
        "tx_rate": int(stop_rate),\
        "duration": end * 1000,\
        "warmup": 0,\
        "num_flows": 300,\
        "size_min": 768,\
        "size_max": 768,\
        "life_min": 1,\
        "life_max": 120,\
        "online": True\
        }))

def decrease_smoothly(q, server, start_rate, stop_rate, steps, duration, margin, end):
    diff = float(start_rate - stop_rate)
    step_size = math.ceil(diff/float(steps))
    duration_per_step = int(math.ceil(duration / float(steps)))
    runduration = int(math.ceil(duration_per_step + margin))
    for rate in xrange(int(stop_rate), int(start_rate), -1 * int(step_size)):
        q.add_job(server, Job(1, {\
            "tx_rate": rate,\
            "duration": runduration * 1000,\
            "warmup": 0,\
            "num_flows": 300,\
            "size_min": 768,\
            "size_max": 768,\
            "life_min": 1,\
            "life_max": 120,\
            "online": True\
            }))
        time.sleep(duration_per_step)
    q.add_job(server, Job(1, {\
        "tx_rate": int(stop_rate),\
        "duration": end * 1000,\
        "warmup": 0,\
        "num_flows": 300,\
        "size_min": 768,\
        "size_max": 768,\
        "life_min": 1,\
        "life_max": 120,\
        "online": True\
        }))


def kill_traffic(q, server):
    q.add_job(server, Job(0, {"stop": True}))


def run_demo_job(q, server, rate, duration = None):
    if not duration:
        duration = 3600 * 1000 # If nothing happens in an hour then we should just
                               # give up.
    q.add_job(server, Job(1, {\
            "tx_rate": rate, \
            "duration": duration, \
            "warmup": 0,\
            "num_flows": 300,\
            "size_min": 512,\
            "size_max": 768,\
            "life_min": 1,\
            "life_max": 10,\
            "online": True
            }))


def run_demo_job_port(q, server, pmin, pmax, rate, duration = None):
    if not duration:
        duration = 24 * 3600 * 1000 # If nothing happens in an hour then we should just
                               # give up.
    q.add_job(server, Job(1, {\
            "tx_rate": rate, \
            "duration": duration, \
            "warmup": 0,\
            "num_flows": 300,\
            "port_min": pmin, \
            "port_max": pmax, \
            "size_min": 512,\
            "size_max": 768,\
            "life_min": 1,\
            "life_max": 5,\
            "online": True
            }))


def run_stress(q):
    server = "s"
    q.add_node(Node(server, "127.0.0.1", 7001))
    while True:
        increase_smoothly(q, server, 20.0, 800.0, 30, 120, 2, 120)
        time.sleep(100)
        decrease_smoothly(q, server, 800.0, 20.0, 30, 120, 2, 120)
        time.sleep(100)
        time.sleep(120)

        increase_smoothly(q, server, 20.0, 800.0, 30, 60, 2, 200)
        time.sleep(185)
        decrease_smoothly(q, server, 800.0, 20.0, 30, 60, 300, 200)
        time.sleep(100)
        time.sleep(120)

        increase_smoothly(q, server, 20.0, 800.0, 5, 15, 2, 30)
        time.sleep(30)
        decrease_smoothly(q, server, 800.0, 20.0, 5, 15, 2, 79)
        time.sleep(60)
        time.sleep(150)


def run_demo(q, generation_function, kill, setup):
    baseline = 250
    spike = 7500
    mid = 1500
    setup()
    while True:
        print "Hello welcome to the E2 demo."
        print "Running baseline traffic"
        generation_function(baseline)
        print "Hit enter to spike"
        raw_input()
        print "Now rapidly spiking traffic"
        generation_function(spike)
        print "Hit enter to decrease midway"
        raw_input()
        generation_function(mid)
        print "OK! Whatever was going on is becoming less of a problem now"
        print "Hit enter to go back to baseline"
        raw_input()
        generation_function(baseline)
        print "Finally things are entirely dying off"
        print "Now let us do that again, but focus on one server"
        print "Hit enter to spike"
        raw_input()
        print "Now rapidly spiking traffic"
        generation_function(spike)
        print "Hit enter to decrease midway"
        raw_input()
        print "OK! Whatever was going on is becoming less of a problem now"
        generation_function(mid)
        print "Hit enter to go back to baseline"
        raw_input()
        print "Finally things are entirely dying off"
        generation_function(baseline)
        print "Hit enter to end demo"
        raw_input()
        print "Thank you. Going back to baseline"
        # kill()
        raw_input()


def run_demo_auto(q, generation_function, kill, setup):
    baseline = 250
    spike = 7500
    mid = 1500
    setup()
    while True:
        print "Hello welcome to the E2 demo."
        print "Running baseline traffic"
        generation_function(baseline)
        print "Hit enter to spike"
        time.sleep(15)
        print "Now rapidly spiking traffic"
        generation_function(spike)
        print "Hit enter to decrease midway"
        time.sleep(15)
        generation_function(mid)
        print "OK! Whatever was going on is becoming less of a problem now"
        print "Hit enter to go back to baseline"
        time.sleep(15)
        generation_function(baseline)
        print "Finally things are entirely dying off"
        print "Now let us do that again, but focus on one server"
        print "Hit enter to spike"
        time.sleep(15)
        print "Now rapidly spiking traffic"
        generation_function(spike)
        print "Hit enter to decrease midway"
        time.sleep(15)
        print "OK! Whatever was going on is becoming less of a problem now"
        generation_function(mid)
        print "Hit enter to go back to baseline"
        time.sleep(15)
        print "Finally things are entirely dying off"
        generation_function(baseline)
        print "Hit enter to end demo"
        time.sleep(15)
        print "Thank you. Killing off traffic, hit enter to get baseline"
        # kill()
        time.sleep(15)


def demo_console(q):
    tenant0_pgen = "t0p"
    q.add_node(Node(tenant0_pgen, "127.0.0.1", 7001))
    print "adding t0p"
    tenant1_pgen = "t1p"
    q.add_node(Node(tenant1_pgen, "127.0.0.1", 7002))
    print "Adding t1p"
    tenant2_pgen = "t2p"
    q.add_node(Node(tenant2_pgen, "127.0.0.1", 7003))
    print "Adding t2p"
    q.add_node(Node(tenant2_pgen, "127.0.0.1", 7004))
    print "Adding t3p"
    t1_background_traffic = 750
    t2_background_traffic = 500
    all_pgens = [tenant0_pgen, tenant1_pgen, tenant2_pgen]
    def t0_traffic(rate):
        run_demo_job_port(q, tenant0_pgen, 1, 1700, rate)
    def t1_traffic(rate):
        run_demo_job_port(q, tenant1_pgen, 5060, 5062, rate)
    def t2_traffic(rate):
        run_demo_job_port(q, tenant2_pgen, 1725, 1726, rate)
    def setup():
        print "NOOP"
    def demo():
        run_demo_job_port(q, tenant1_pgen, 5060, 5062, t1_background_traffic, \
                duration = 24 * 3600 * 1000)
        run_demo_job_port(q, tenant2_pgen, 1725, 1726, t2_background_traffic, \
                duration = 24 * 3600 * 1000)
        run_demo(q, t0_traffic, kill, setup)
    def demo_auto():
        run_demo_job_port(q, tenant1_pgen, 5060, 5062, t1_background_traffic, \
                duration = 24 * 3600 * 1000)
        run_demo_job_port(q, tenant2_pgen, 1725, 1726, t2_background_traffic, \
                duration = 24 * 3600 * 1000)
        run_demo_auto(q, t0_traffic, kill, setup)
    def kill():
        for pgen in all_pgens:
            kill_traffic(q, pgen)
    def kill_t0():
        kill_traffic(q, tenant0_pgen)
    def kill_t1():
        kill_traffic(q, tenant0_pgen)
    def kill_t2():
        kill_traffic(q, tenant0_pgen)
    code.interact(local=dict(globals(), **locals()))

def main():
    q_ip = IP
    q_port = PORT
    q_nodes_file = q_jobs_file = None

    parser = argparse.ArgumentParser(
        description="pktgen_scheduler schedules jobs for pktgen_servers")

    parser.add_argument('-p', '--port', type=int, help='the port pktgen_scheduler will listen on')
    parser.add_argument('-n', '--nodes', type=str, help='nodes json file to load')
    parser.add_argument('-j', '--jobs', type=str, help='jobs json file to load')
    parser.add_argument('-i', '--interactive', action="store_true", help='interactive mode')
    parser.add_argument('-d', '--demo', action="store_true", help='demo mode')

    args = parser.parse_args()

    if args.port:
        q_port = args.port

    if args.nodes:
        q_nodes_file = args.nodes

    if args.jobs:
        q_jobs_file = args.jobs

    q = Q(q_ip, q_port, q_nodes_file, q_jobs_file)
    q.start()
    if args.demo:
        demo_console(q)
    else:

        code.interact(local=dict(globals(), **locals()))

    q.stop()


if __name__ == '__main__':
    main()
