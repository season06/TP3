# TP3 - NoSQL vs BlockChain

## Environment
- OS: Ubuntu 21.04
- CPU: 2 Cores
- RAM: 4 GB
## Prerequest

- Install Docker & Docker Compose  
    > Follow the instructions from the official document  
    - [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)  
    - [Install and Use Docker Compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)

## NoSQL - Redis

### Execute Redis by Docker
```bash
cd ./redis-cluster
docker-compose up --scale redis-master=1 --scale redis-replica=3 -d
```
### Install YSCB
```bash
## Dependency
sudo apt-get install maven

## Install
curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/ycsb-0.17.0.tar.gz
tar xfvz ycsb-0.17.0.tar.gz

cd ~/ycsb-0.17.0

# Load
./bin/ycsb.sh load redis -s -P ~/redis_cluster/workload_50_50 -p "redis.host=127.0.0.1" -p "redis.port=6379"
# Run
./bin/ycsb.sh run redis -s -P ~/redis_cluster/workload_50_50 -p "redis.host=127.0.0.1" -p "redis.port=6379" > ~/report/ycsb/output_50_50.txt
```
- References
    - [YCSB (GitHub)](https://github.com/brianfrankcooper/YCSB)
    - [Core Workloads](https://github.com/brianfrankcooper/YCSB/wiki/Core-Workloads)
    - [Running a Workload](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
## HyperLedger
```bash
# Dependency
sudo apt-get install build-essential nodejs npm

git clone https://github.com/hyperledger/caliper-benchmarks.git
cd caliper-benchmarks/
git checkout d02cc8bbc17afda13a0d3af1122d43bfbfc45b0a

npm init -y
npm install --only=prod @hyperledger/caliper-cli@0.4

# Generate peerx`
cd networks/fabric/config_solo_raft/
./generate.sh

# If occurs an error about `Error while performing "install"`, refer: https://github.com/hyperledger/caliper/issues/955
docker pull hyperledger/fabric-ccenv:1.4.4
docker tag hyperledger/fabric-ccenv:1.4.4 hyperledger/fabric-ccenv:latest

curl https://raw.githubusercontent.com/creationix/nvm/v0.25.0/install.sh | bash

# Change versions of node(12.22.12) and npm(6.14.16)
nvm install 12

# Change to python2, refer to the instructions below to install virturalenv.
source ~/py2/bin/activate

# If `grpc_node.node` not found, refer: https://blog.csdn.net/bean_business/article/details/108807977
npm rebuild grpc --force

# Run
cd ~/caliper-benchmarks/
npx caliper bind --caliper-bind-sut fabric:1.4.11
npm install --save fabric-client fabric-ca-client
# Edit content in config.yaml
sudo npx caliper launch manager --caliper-workspace . --caliper-benchconfig benchmarks/samples/fabric/marbles/config.yaml --caliper-networkconfig networks/fabric/v1/v1.4.4/2org1peercouchdb_raft/fabric-go-tls-solo.yaml
```
- Install virturalenv for multiple python versions
```bash
sudo api-get install python2
pip install virtualenv

# Create the environment for python2
virtualenv -p /usr/bin/python2 py2

# Activate a virtual environment
source ~/py2/bin/activate
python -V

# Leave the virtual environment
deactivate
```
- References
    - [Hyperledger Fabric Docs](https://hyperledger-fabric.readthedocs.io/en/release-2.5/install.html)
    - [Hyperledger Caliper Docs](https://hyperledger.github.io/caliper/v0.5.0/installing-caliper/)

## Get Container Metrics
- Use `docker stats` to get the matrics of the container in half a second
- Use bash script to collect output of `docker stats`
    ```bash
    chmod -x collect_docker_matrics.sh

    # Get container id
    docker ps -a

    # ./collect_docker_matrics {Container_ID} {Output_file}
    ./collect_docker_matrics xxxxxxxxxxxx matrics.txt
    ```
- Use `matplotlib.pyplot.plot`, a Python library, to visualize