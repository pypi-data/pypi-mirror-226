import csv
import glob
import re
import os.path

from src.pquisby.lib.pricing.cloud_pricing import get_cloud_pricing, get_cloud_cpu_count
from src.pquisby.lib.util import read_config


def linpack_format_data(**kwargs):
    """
    Add data into format to be shown in spreadsheets
    Supports linpack like data. eg: autohpl
    """
    region = read_config("/Users/soumyasinha/.config/quisby/config.ini","cloud","region")
    cloud_type = read_config("/Users/soumyasinha/.config/quisby/config.ini","cloud","cloud_type")
    os_release =read_config("/Users/soumyasinha/.config/quisby/config.ini","test","OS_RELEASE")
    results = kwargs["results"] if kwargs["results"] else []
    system_name = kwargs["system_name"] if kwargs["system_name"] else None
    dataset_name = kwargs["dataset_name"]
    if kwargs["gflops"]:
        gflops = float(kwargs["gflops"])
    else:
        return None

    results_json = kwargs["results_json"] if kwargs["results_json"] else []
    metrics = ["gflops", "gflop_scaling", "price_perf"]

    price_per_hour = get_cloud_pricing(
        system_name, region, cloud_type.lower()
    )

    no_of_cores = get_cloud_cpu_count(
        system_name, region, cloud_type.lower()
    )
    price_perf = float(gflops) / float(price_per_hour)
    gflop_scaling = 1

    for metric in metrics:
        linpack_test = {}
        linpack_test["vm_name"] = system_name
        linpack_test["test_name"] = metric
        linpack_test["metrics_unit"] = metric
        linpack_test["instances"] = []
        if metric == "gflops" :
            value = gflops
        elif metric == "gflop_scaling":
            value = gflop_scaling
        else:
            value = price_perf
        linpack_test["instances"].append({"value": value,"dataset_name":dataset_name})
        results_json["data"].append(linpack_test)

    results.append(
        [
            "System",
            "Cores",
            f"GFLOPS-{os_release}",
            f"GFLOP Scaling-{os_release}",
            "Cost/hr",
            f"Price/Perf-{os_release}",
        ]
    )
    results.append(
        [
            system_name,
            no_of_cores,
            gflops,
            1,
            price_per_hour,
            float(gflops) / float(price_per_hour),
        ]
    )

    return results,results_json


def extract_linpack_data(system_name, data):
    """
    Make shift function to handle linpack summary data
    till a resolution is reached
    """

    results = []
    no_of_cores = None
    gflops = None
    results_json = {"dataset_name":"dataset_1","data":[]}
    with open(data) as csv_file:
        data = list(csv.DictReader(csv_file, delimiter=":"))

    last_row = data[-1]
    gflops = last_row["MB/sec"]
    threads = last_row["threads"]

    if gflops:
        results = linpack_format_data(
            results_json =results_json,
            results=results,
            system_name="n2-standard-128",
            dataset_name=system_name,
            no_of_cores=no_of_cores,
            gflops=gflops,
        )

        return results


#extract_linpack_data("/Users/soumyasinha/Workspace/2022/rocky_rhel_gvnic/rhel_9_1/n2-standard-128/pbench-user-benchmark_sousinha_linpack_test_2023.07.16T05.31.07/results_linpack.csv","n2-standard-128")
#[['System', 'Cores', 'GFLOPS-9.1', 'GFLOP Scaling-9.1', 'Cost/hr', 'Price/Perf-9.1'], ['n2-standard-128', 128, 2953.0, 1, 0.031611, 93416.84856537281]]
#[['System', 'Cores', 'GFLOPS-9.1', 'GFLOP Scaling-9.1', 'Cost/hr', 'Price/Perf-9.1'], ['n2-standard-128', 128, 2953.0, 1, 0.031611, 93416.84856537281]]

#extract_linpack_data("dataset_1","/Users/soumyasinha/Workspace/2022/rocky_rhel_gvnic/rhel_9_1/n2-standard-128/pbench-user-benchmark_sousinha_linpack_test_2023.07.16T05.31.07/results_linpack.csv")