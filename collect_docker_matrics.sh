#!/bin/sh

echo "CPU,Mem,Net,Block" | tee -a "$2"

# First, start the container
CONTAINER_ID=$1

# Then start watching that it's running (with inspect)
while [ "$(docker inspect -f {{.State.Running}} $CONTAINER_ID 2>/dev/null)" = "true" ]; do
    # And while it's running, check stats
    #docker stats $CONTAINER_ID 2>&1 | tee "$1"
    docker stats --format "{{.CPUPerc}},{{.MemUsage}},{{.NetIO}},{{.BlockIO}}" $CONTAINER_ID 2>&1 | tee -a "$2"
done
