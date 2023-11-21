# TP3

## Environment
- OS: Ubuntu 21.04
- CPU: 2 core
- RAM: 4 GB
## Prerequest

- Install Docker & Docker Compose  
    | Follow the instruction from official document  
    - [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)  
    - [Install and Use Docker Compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)

## NoSQL - Redis

### Execute Redis by Docker
```bash
cd ./redis-cluster
docker-compose up --scale redis-master=1 --scale redis-replica=3
```
### Install YSCB
```bash
## Dependency
sudo apt-get install maven

## Install
curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/ycsb-0.17.0.tar.gz
tar xfvz ycsb-0.17.0.tar.gz

cd ycsb-0.17.0

# Load
./bin/ycsb.sh load redis -s -P workloads/workloada -p "redis.host=127.0.0.1" -p "redis.port=6379"
# Run
./bin/ycsb.sh run redis -s -P workloads/workloada -p "redis.host=127.0.0.1" -p "redis.port=6379" > output.txt
```
- Reference
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

# Generate peer
cd networks/fabric/config_solo_raft/
./generate.sh

# If if occurs an error about GOROOT
# https://github.com/hyperledger/caliper/issues/955
docker pull hyperledger/fabric-ccenv:1.4.4
docker tag hyperledger/fabric-ccenv:1.4.4 hyperledger/fabric-ccenv:latest

npm install --save fabric-client fabric-ca-client
curl https://raw.githubusercontent.com/creationix/nvm/v0.25.0/install.sh | bash

# Change node(12.22.12) and nvm(6.14.16) version
npm install 12

# Change to python2
source ~/py2/bin/activate

# If `grpc_node.node not` found
# https://blog.csdn.net/bean_business/article/details/108807977
npm rebuild grpc --force

# Run
cd ~/tp3/caliper-benchmarks/
npx caliper bind --caliper-bind-sut fabric:1.4.11
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
- Reference
    - [Hyperledger Fabric Docs](https://hyperledger-fabric.readthedocs.io/en/release-2.5/install.html)
    - [Hyperledger Caliper Docs](https://hyperledger.github.io/caliper/v0.5.0/installing-caliper/)