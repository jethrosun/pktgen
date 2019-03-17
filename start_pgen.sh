#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	echo "Run this as root"
	exit
fi
TENANT_0_PORT=7001
TENANT_0_PFX="ten0"
TENANT_1_PORT=7002
TENANT_1_PFX="ten1"
TENANT_2_PORT=7003
TENANT_2_PFX="ten2"
stdbuf -o0 -e0 build/pktgen -c 0x3 -w 01:00.0 --file-prefix $TENANT_0_PFX --socket-mem=20,0 -- $TENANT_0_PORT 0.0.0.0 &> /var/log/t0tg &
T0_PID=$!
stdbuf -o0 -e0 build/pktgen -c 0xc -w 01:00.1 --file-prefix $TENANT_1_PFX --socket-mem=20,0 -- $TENANT_1_PORT 0.0.0.0 &> /var/log/t1tg &
T1_PID=$!
#stdbuf -o0 -e0 build/pktgen -c 0x30 -w 01:00.2 --file-prefix $TENANT_2_PFX --socket-mem=20,0 -- $TENANT_2_PORT 0.0.0.0 &> /var/log/t2tg &
#T2_PID=$!

python scheduler/pktgen_scheduler.py -d

#kill $T0_PID
#kill $T1_PID
#kill $T2_PID
wait
