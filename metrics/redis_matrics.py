import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

def to_dataframe(string):
    df = pd.read_csv(io.StringIO(string))
    for i in df:
        df[i.strip()] = df.pop(i)
    df['CPU'] = df['CPU'].str.replace('%', '').astype(float)
    df['Mem'] = df['Mem'].str.replace(
        '[a-zA-Z]+.\/.*', '', regex=True).astype(float)
    df['Net'] = df['Net'].str.replace(
        '[a-zA-Z]+.\/.*', '', regex=True).astype(float)
    df['Block'] = df['Block'].str.replace(
        '[a-zA-Z]+.\/.*', '', regex=True).astype(float)

    return df


def range_with_floats(start, stop, step):
    while stop > start:
        yield start
        start += step


def find_max(a, b):
    if a > b:
        return a
    return b


def generate_cpu(sec, master_arr, replica_arr):
    plt.figure(figsize=(4, 2.5))
    plt.plot(sec, master_arr, linestyle='-', label='master')
    plt.plot(sec, replica_arr, linestyle='-', label='replica')

    plt.xticks(np.arange(min(sec), max(sec)+1, 0.5))
    plt.xlim(0, max(sec))
    plt.ylim(0, find_max(max(master_arr), max(replica_arr)) + 5)
    plt.xlabel('Time (seconds)')

    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage')

    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()


def generate_mem(sec, master_arr, replica_arr):
    plt.figure(figsize=(4, 2.5))
    plt.plot(sec, master_arr, linestyle='-', label='master')
    plt.plot(sec, replica_arr, linestyle='-', label='replica')

    plt.xticks(np.arange(min(sec), max(sec)+1, 0.5))
    plt.xlim(0, max(sec))
    plt.ylim(0, find_max(max(master_arr), max(replica_arr)) + 10)
    plt.xlabel('Time (seconds)')

    plt.ylabel('Memory Usage (MiB)')
    plt.title('Memory Usage')

    plt.legend()
    plt.tight_layout()
    plt.show()


def generate_net(sec, master_arr, replica_arr):
    for i in range(0, len(master_arr)):
        if master_arr[i] < 25:
            master_arr[i] *= 1000
    for i in range(0, len(replica_arr)):
        if replica_arr[i] < 25:
            replica_arr[i] *= 1000

    plt.figure(figsize=(4, 2.5))
    plt.plot(sec, master_arr, linestyle='-', label='master')
    plt.plot(sec, replica_arr, linestyle='-', label='replica')

    plt.xticks(np.arange(min(sec), max(sec)+1, 0.5))
    plt.xlim(0, max(sec))
    plt.ylim(0, find_max(max(master_arr), max(replica_arr)) + 1000)
    plt.xlabel('Time (seconds)')

    plt.ylabel('Net I/O (KB)')
    plt.title('Net I/O')

    plt.legend()
    plt.tight_layout()
    plt.show()


def generate_block(sec, master_arr, replica_arr):
    plt.figure(figsize=(4, 2.5))
    plt.plot(sec, master_arr, linestyle='-', label='master')
    plt.plot(sec, replica_arr, linestyle='-', label='replica')

    plt.xticks(np.arange(min(sec), max(sec)+1, 0.5))
    plt.xlim(0, max(sec))
    plt.ylim(0, find_max(max(master_arr), max(replica_arr)) + 20)
    plt.xlabel('Time (seconds)')

    plt.ylabel('Block I/O (KB)')
    plt.title('Block I/O')

    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    master_matrics = open('./0_100/redis_master.txt', 'r').read()
    replica_matrics = open('./0_100/redis_replica.txt', 'r').read()

    master_df = to_dataframe(master_matrics)
    replica_df = to_dataframe(replica_matrics)

    master = {
        'cpu': master_df['CPU'].values.tolist(),
        'mem': master_df['Mem'].values.tolist(),
        'net': master_df['Net'].values.tolist(),
        'block': master_df['Block'].values.tolist()
    }
    replica = {
        'cpu': replica_df['CPU'].values.tolist(),
        'mem': replica_df['Mem'].values.tolist(),
        'net': replica_df['Net'].values.tolist(),
        'block': replica_df['Block'].values.tolist()
    }

    sec = list(range_with_floats(0, len(master['cpu'])/2, 0.5))

    generate_cpu(sec, master['cpu'], replica['cpu'])
    generate_mem(sec, master['mem'], replica['mem'])
    generate_net(sec, master['net'], replica['net'])
    generate_block(sec, master['block'], replica['block'])


if __name__ == "__main__":
    main()
