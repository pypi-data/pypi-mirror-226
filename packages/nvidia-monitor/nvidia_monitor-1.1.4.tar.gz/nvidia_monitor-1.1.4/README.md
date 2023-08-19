# PyPI.nvidia-monitor

# nvidia_monitor.gpu.status
<details>
<summary> 0.1.2 </summary>
* First deplotment of Status class   
* Status class use STATUS_QUERY list at queries.py file.   
* User can add any keys supported by nvidia-smi --query-gpu. (Refer to nvidia-smi --help-query-gpu)


Example)
```python
from nvidia_monitor.gpu.status import Status

status = Status()
list_dict_output = status.get_gpu_status(verbose=False)

for output in list_dict_output:
    # print(output.keys())
    print(output)
```
Output:
```bash
{'index': '0', 'timestamp': '2023/08/19 14:53:46.783', 'driver_version': '535.86.05', 'count': '1', 'name': 'NVIDIA GeForce RTX 3090', 'serial': '12345678901234', 'uuid': 'GPU-12345678-1234-1234-1234-123456789012', 'display_mode': 'Enabled', 'persistence_mode': 'Disabled', 'fan.speed': '62 %', 'pstate': 'P2', 'memory.total': '24576 MiB', 'memory.used': '18620 MiB', 'memory.free': '5605 MiB', 'utilization.gpu': '100 %', 'temperature.gpu': '82', 'power.draw': '335.89 W', 'power.draw.average': '335.89 W', 'power.limit': '350.00 W', 'power.max_limit': '350.00 W'}
```
* All the keys that you can use are at ***queries.py*** **STATUS_QUERY**. You can add additional keys in that file.

</details>