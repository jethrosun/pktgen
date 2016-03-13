#!/bin/bash
TENANT_0_PORT=7001
TENANT_0_PFX="ten0"
TENANT_1_PORT=7002
TENANT_1_PFX="ten1"
TENANT_2_PORT=7003
TENANT_2_PFX="ten2"
pkill pktgen
stdbuf -o0 -e0 build/pktgen -c 0x3 -w 07:00.0 --file-prefix $TENANT_0_PFX --socket-mem=20,0 -- $TENANT_0_PORT 0.0.0.0 &> /var/log/t0tg &

stdbuf -o0 -e0 build/pktgen -c 0xc -w 07:00.1 --file-prefix $TENANT_1_PFX --socket-mem=20,0 -- $TENANT_1_PORT 0.0.0.0 &> /var/log/t1tg &

stdbuf -o0 -e0 build/pktgen -c 0x30 -w 07:00.2 --file-prefix $TENANT_2_PFX --socket-mem=20,0 -- $TENANT_2_PORT 0.0.0.0 &> /var/log/t2tg &

