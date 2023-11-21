# Reports

> Use https://htmlpreview.github.io/ to preview html

## YCSB - Performance Statistics
The default is to produce average, min, max, 95th and 99th percentile latency for each operation type (read, update, etc.), a count of the return codes for each operation, and a histogram of latencies for each operation.

> Ref: [Running a Workload - Step 6](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)

The core workloads consist of six workloads:

- Workload A: Update heavy workload
    > 50/50 reads and writes
- Workload B: Read mostly workload
    > 95/5 reads/write
- Workload C: Read only
    > 100% read
- Workload D: Read latest workload
    > new records are inserted
- Workload E: Short ranges
    > short ranges of records are queried, instead of individual records
- Workload F: Read-modify-write
    > the client will read a record, modify it, and write back the changes

> Ref: [Core Workloads](https://github.com/brianfrankcooper/YCSB/wiki/Core-Workloads)

## Caliper - Benchmark Results
The resulting report will detail the following items for each benchmark round:

- Name - the round name from the benchmark configuration file
- Succ/Fail - the number of successful/failing transactions
- Send Rate - the rate at which caliper issued the transactions
- Latency (max/min/avg) - statistics relating to the time taken in seconds between issuing a transaction and receiving a response
- Throughput - the average number of transactions processed per second

> Ref: [Setting up and Running a Performance Benchmark on an existing network](https://hyperledger.github.io/caliper/vNext/fabric-tutorial/tutorials-fabric-existing/#step-5---run-the-caliper-benchmark)