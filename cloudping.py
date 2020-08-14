# coding: utf-8

import sys
import os
import argparse
import requests

import datetime
import socket

from multiprocessing import Pool
import pandas as pd

gcp_latency = [
    {"name": "global", "ip": "35.186.221.153"},
    {"name": "asia-east1", "ip": "104.155.201.52"},
    {"name": "asia-east2", "ip": "35.220.162.209"},
    {"name": "asia-northeast1", "ip": "104.198.86.148"},
    {"name": "asia-northeast2", "ip": "34.97.196.51"},
    {"name": "asia-south1", "ip": "35.200.186.152"},
    {"name": "asia-southeast1", "ip": "35.185.179.198"},
    {"name": "australia-southeast1", "ip": "35.189.6.113"},
    {"name": "europe-north1", "ip": "35.228.170.201"},
    {"name": "europe-west1", "ip": "104.199.82.109"},
    {"name": "europe-west2", "ip": "35.189.67.146"},
    {"name": "europe-west3", "ip": "35.198.78.172"},
    {"name": "europe-west4", "ip": "35.204.93.82"},
    {"name": "europe-west6", "ip": "34.65.3.254"},
    {"name": "northamerica-northeast1", "ip": "35.203.57.164"},
    {"name": "southamerica-east1", "ip": "35.198.10.68"},
    {"name": "us-central1", "ip": "104.197.165.8"},
    {"name": "us-east1", "ip": "104.196.161.21"},
    {"name": "us-east4", "ip": "35.186.168.152"},
    {"name": "us-west1", "ip": "104.199.116.74"},
    {"name": "us-west2", "ip": "35.236.45.25"}
]

aws_latency = [
    {"name": "eu-west-1", "ip": "52.218.41.35"},
    {"name": "eu-north-1", "ip": "52.95.170.21"},
    {"name": "eu-west-3", "ip": "52.95.155.53"},
    {"name": "eu-central-1", "ip": "52.219.72.155"},
    {"name": "eu-west-2", "ip": "52.95.150.48"},
    {"name": "ap-northeast-1", "ip": "52.219.136.10"},
    {"name": "ap-northeast-2", "ip": "52.219.56.145"},
    {"name": "ap-southeast-1", "ip": "52.219.132.158"},
    {"name": "ap-southeast-2", "ip": "52.95.134.239"},
    {"name": "ap-south-1", "ip": "52.219.66.105"},
    {"name": "ca-central-1", "ip": "52.95.147.180"},
    {"name": "sa-east-1", "ip": "52.95.164.34"},
    {"name": "us-east-2", "ip": "52.219.80.170"},
    {"name": "us-west-1", "ip": "52.219.113.8"},
    {"name": "us-west-2", "ip": "52.218.220.144"}
]

azure_latency = [
    {"name": "westeurope", "ip": "52.239.142.132"},
    {"name": "northeurope", "ip": "52.239.136.37"},
    {"name": "centralus", "ip": "52.239.159.84"},
    {"name": "eastus", "ip": "52.239.220.32"},
    {"name": "westus", "ip": "52.239.236.228"},
    {"name": "northcentralus", "ip": "52.239.186.132"},
    {"name": "francecentral", "ip": "52.239.134.100"},
    {"name": "koreasouth", "ip": "52.231.168.142"},
    {"name": "uksouth", "ip": "52.239.231.164"},
    {"name": "australiacentral", "ip": "52.239.216.36"},
    {"name": "westindia", "ip": "104.211.168.16"},
    {"name": "ukwest", "ip": "51.140.232.142"}
]


def parser_arguments():
    """
    Function to parse all command line arguments.
    """
    parser = argparse.ArgumentParser("Get Latency from list of dict")
    parser.add_argument("-o", "--output", type=str,
                        help="Format of the output", default="table")
    parser.add_argument("--cloud", type=str,
                        help="Clouder, can take value \"gcp\" / \"aws\" \"azure\"", choices=["gcp", "aws", "azure"], required=False)
    args = parser.parse_args()
    return args


def output_result(dataset, type_output):
    # Print the result in table
    df = pd.DataFrame(dataset).reindex(columns=['Name', 'IP', 'Latency in ms'])
    df.index = df.index + 1
    if type_output == "table":
        print(df)
    elif type_output == "csv":
        print(df.to_csv())
    elif type_output == "html":
        print(df.to_html())
    elif type_output == "json":
        print(df.to_json())


def perform_get(server):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = (f"{server['ip']}", 80)

    time_before = datetime.datetime.now()

    a_socket.connect_ex(location)

    time_after = datetime.datetime.now()
    a_socket.close()
    time_taken = time_after-time_before

    return {"Name": server['name'], "IP": server['ip'], "Latency in ms": time_taken.total_seconds()*1000}


def get_all_latency(server_to_get_latency):
    # Define Pool Size of maximal concurrent processes
    pool = Pool(os.cpu_count())

    # get all value concurrently
    result = pool.map(perform_get, server_to_get_latency)

    pool.close()
    pool.join()

    # Sort by latency
    dataset = sorted(result, key=lambda i: (i['Latency in ms']))

    return dataset


def main():
    args = parser_arguments()
    if args.cloud:
        if args.cloud == "gcp":
            dataset = get_all_latency(gcp_latency)
        if args.cloud == "aws":
            dataset = get_all_latency(aws_latency)
        if args.cloud == "azure":
            dataset = get_all_latency(azure_latency)

    # Test if dataset variable is defined
    try:
        dataset
        output_result(dataset, args.output)
    except NameError:
        print("No test latency of clouder")


# Main
if __name__ == "__main__":
    main()

    # Exiting
    sys.exit(0)
