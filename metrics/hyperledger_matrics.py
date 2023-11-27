import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

def to_dataframe(string):
    df = pd.read_csv(io.StringIO(string))
    for i in df:
        df[i.strip()] = df.pop(i)
    df['CPU'] = df['CPU'].str.replace('%', '').astype(float)
    df['Mem'] = df['Mem'].str.replace('[a-zA-Z]+.\/.*', '', regex=True).astype(float)
    df['Net'] = df['Net'].str.replace('[a-zA-Z]+.\/.*', '', regex=True).astype(float)
    df['Block'] = df['Block'].str.replace('[a-zA-Z]+.\/.*', '', regex=True).astype(float)

    return df

def range_with_floats(start, stop, step):
    while stop >= start:
        yield start
        start += step

def find_max_value(a, b, c):
    max_ab = a if a > b else b
    max_value = max_ab if max_ab > c else c
    return max_value


def generate_cpu(sec, peer_arr, order_arr, db_arr):
    plt.figure(figsize=(4, 2.5))
    plt.plot(sec, peer_arr, linestyle='-', label='peer')
    plt.plot(sec, order_arr, linestyle='-', label='order')
    plt.plot(sec, db_arr, linestyle='-', label='db')

    plt.xticks(np.arange(min(sec), max(sec)+1, 40.0))
    plt.xlim(0, max(sec))
    plt.ylim(0, find_max_value(max(peer_arr), max(order_arr), max(db_arr)) + 10)
    plt.xlabel('Time (seconds)')

    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage')

    plt.legend(loc='upper left', fontsize=8)
    plt.tight_layout()
    plt.show()


def generate_mem(sec, peer_arr, order_arr, db_arr):
    plt.figure(figsize=(4, 2.5))
    plt.plot(sec, peer_arr, linestyle='-', label='peer')
    plt.plot(sec, order_arr, linestyle='-', label='order')
    plt.plot(sec, db_arr, linestyle='-', label='db')

    plt.xticks(np.arange(min(sec), max(sec)+1, 40.0))
    plt.xlim(0, max(sec))
    plt.ylim(0, find_max_value(max(peer_arr), max(order_arr), max(db_arr)) + 10)
    plt.xlabel('Time (seconds)')

    plt.ylabel('Memory Usage (MiB)')
    plt.title('Memory Usage')

    plt.legend(loc='upper left', fontsize=8)
    plt.tight_layout()
    plt.show()


def generate_net(sec, peer_arr, order_arr, db_arr):
    for i in range(0, len(peer_arr)):
        if peer_arr[i] < 5:
            peer_arr[i] *= 1000
    for i in range(0, len(order_arr)):
        if order_arr[i] < 5:
            order_arr[i] *= 1000
    for i in range(0, len(db_arr)):
        if db_arr[i] < 5:
            db_arr[i] *= 1000

    plt.figure(figsize=(4, 2.5))
    plt.plot(sec, peer_arr, linestyle='-', label='peer')
    plt.plot(sec, order_arr, linestyle='-', label='order')
    plt.plot(sec, db_arr, linestyle='-', label='db')

    plt.xticks(np.arange(min(sec), max(sec)+1, 40.0))
    plt.xlim(0, max(sec))
    plt.ylim(0, find_max_value(max(peer_arr), max(order_arr), max(db_arr)) + 500)
    plt.xlabel('Time (seconds)')

    plt.ylabel('Net I/O (KB)')
    plt.title('Net I/O')

    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()


def generate_block(sec, peer_arr, order_arr, db_arr):
    plt.figure(figsize=(4, 2.5))
    plt.plot(sec, peer_arr, linestyle='-', label='peer')
    plt.plot(sec, order_arr, linestyle='-', label='order')
    plt.plot(sec, db_arr, linestyle='-', label='db')

    plt.xticks(np.arange(min(sec), max(sec)+1, 40.0))
    plt.xlim(0, max(sec))
    plt.ylim(0, find_max_value(max(peer_arr), max(order_arr), max(db_arr)) + 100)
    plt.xlabel('Time (seconds)')

    plt.ylabel('Block I/O (KB)')
    plt.title('Block I/O')

    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()

def main():
    peer_matrics = open('./0_100/hyperledger_peer.txt', 'r').read()
    order_matrics = open('./0_100/hyperledger_order.txt', 'r').read()
    db_matrics = open('./0_100/hyperledger_db.txt', 'r').read()

    peer_df = to_dataframe(peer_matrics)
    peer_cpu_arr = peer_df['CPU'].values.tolist()
    peer_mem_arr = peer_df['Mem'].values.tolist()
    peer_net_arr = peer_df['Net'].values.tolist()
    peer_block_arr = peer_df['Block'].values.tolist()

    order_df = to_dataframe(order_matrics)
    order_cpu_arr = order_df['CPU'].values.tolist()
    order_mem_arr = order_df['Mem'].values.tolist()
    order_net_arr = order_df['Net'].values.tolist()
    order_block_arr = order_df['Block'].values.tolist()

    db_df = to_dataframe(db_matrics)
    db_cpu_arr = db_df['CPU'].values.tolist()
    db_mem_arr = db_df['Mem'].values.tolist()
    db_net_arr = db_df['Net'].values.tolist()
    db_block_arr = db_df['Block'].values.tolist()

    sec = list(range_with_floats(0, len(order_cpu_arr)//2, 0.5))

    generate_cpu(sec, peer_cpu_arr, order_cpu_arr, db_cpu_arr)
    generate_mem(sec, peer_mem_arr, order_mem_arr, db_mem_arr)
    generate_net(sec, peer_net_arr, order_net_arr, db_net_arr)
    generate_block(sec, peer_block_arr, order_block_arr, db_block_arr)

main()
