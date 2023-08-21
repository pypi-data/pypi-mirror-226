from itertools import groupby

from src.pquisby.lib.util import process_instance, mk_int


def create_summary_linpack_data(results,OS_RELEASE):

    sorted_results = []

    results = list(filter(None, results))
    header_row = [results[0]]
    results = [row for row in results if row[0] != "System"]

    results.sort(key=lambda x: str(process_instance(x[0], "family", "version", "feature")))

    for _, items in groupby(results, key=lambda x: process_instance(x[0], "family", "version", "feature")):
        items = list(items)
        sorted_data = sorted(items, key=lambda x: mk_int(process_instance(x[0], "size")))
        cpu_scale, base_gflops = None, None
        for index, row in enumerate(sorted_data):
            if not cpu_scale and not base_gflops:
                cpu_scale = int(row[1])
                base_gflops = float(row[2])
            else:
                try:
                    cpu_scaling = int(row[1]) - cpu_scale
                except ZeroDivisionError:
                    cpu_scaling = 0
                gflops_scaling = float(row[2]) / (int(row[1]) - cpu_scale) / base_gflops if cpu_scaling !=0 else 1
                sorted_data[index][3] = format(gflops_scaling, ".4f")
        sorted_results += header_row + sorted_data

    return sorted_results


create_summary_linpack_data([['System', 'Cores', 'GFLOPS-9.1', 'GFLOP Scaling-9.1', 'Cost/hr', 'Price/Perf-9.1'], ['n2-standard-128', 128, 2953.0, 1, 0.031611, 93416.84856537281]],9.1)
#[['System', 'Cores', 'GFLOPS-9.1', 'GFLOP Scaling-9.1', 'Cost/hr', 'Price/Perf-9.1'], ['n2-standard-128', 128, 2953.0, 1, 0.031611, 93416.84856537281]]