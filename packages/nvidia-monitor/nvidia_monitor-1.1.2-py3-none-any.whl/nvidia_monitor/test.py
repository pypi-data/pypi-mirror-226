# %%
from gpu.process import Process

process = Process()
process.keys()
process.get_process_info()
# %%
from gpu.status import Status

status = Status()
list_dict_output = status.get_gpu_status(verbose=False)

for output in list_dict_output:
    # print(output.keys())
    print(output)