from pathlib import Path
import tarfile
import json
from pquisby.lib.post_processing import BenchmarkName, InputType, QuisbyProcessing

tarball_path = Path('/home/siddardh/test-staging/pbench/uperf_test-quisby_2023.06.20T13.50.47.tar.xz')
tar = tarfile.open(tarball_path, "r:*")
file= tar.extractfile('uperf_test-quisby_2023.06.20T13.50.47/result.csv').read().decode()

tarball_path1 = Path('/home/siddardh/test-staging/pbench/uperf_test-quisby_2023.06.20T14.00.23.tar.xz')
tar1 = tarfile.open(tarball_path1, "r:*")
file1= tar1.extractfile('uperf_test-quisby_2023.06.20T14.00.23/result.csv').read().decode()

json_file={}

json_file['ds1']=file
json_file['ds2']=file1

# json_data = QuisbyProcessing().extract_data(test_name=BenchmarkName.UPERF,dataset_name="ds1", input_type=InputType.STREAM, data=file)
json_data = QuisbyProcessing().compare_csv_to_json(benchmark_name=BenchmarkName.UPERF, input_type=InputType.STREAM, data_stream=json_file)

a=json.dumps(json_data)
print(a)