import subprocess
from .status import Status
from .queries import STATUS_QUERY, COMPUTE_QUERY
from typing import Union

class Process(object):
    def __init__(
        self,
    ):
        assert 'index' in STATUS_QUERY
        assert 'serial' in STATUS_QUERY
        assert 'uuid' in STATUS_QUERY
        assert 'memory.total' in STATUS_QUERY
        assert 'memory.used' in STATUS_QUERY
        
        status = Status()
        self.gpu_index = list()
        self.gpu_serial = list()
        self.gpu_uuid = list()
        self.memory_total = list()
        self.memory_used = list()
        self.count:int = 0
        
        self.uuid2index = dict()
        self.serial2index = dict()
        
        gpu_status_outputs = status.get(verbose=False)
        for gpu_status in gpu_status_outputs:
            self.gpu_index.append(gpu_status['index'])
            self.gpu_serial.append(gpu_status['serial'])
            self.gpu_uuid.append(gpu_status['uuid'])
            self.memory_total.append(gpu_status['memory.total'])
            self.memory_used.append(gpu_status['memory.used'])
            self.count = int(gpu_status['count'])
            self.uuid2index[gpu_status['uuid']] = gpu_status['index']
            self.serial2index[gpu_status['serial']] = gpu_status['index']
            
    def _get_status_query(
        self,
        gpu_index:Union[int, list]=None,
    )->str:
        _str_query = ','.join(COMPUTE_QUERY)
        if gpu_index is None:
            _str_query = f"nvidia-smi --query-compute-apps={_str_query} --format=csv"
        elif isinstance(gpu_index, int):
            _str_query = f"nvidia-smi --query-compute-apps={_str_query} --format=csv -i {gpu_index}"
        elif isinstance(gpu_index, list):
            gpu_index_list = ''
            for i in gpu_index:
                gpu_index_list += str(i) + ','
            gpu_index = gpu_index_list[:-1]
            _str_query = f"nvidia-smi --query-compute-apps={_str_query} --format=csv -i {','.join(gpu_index)}"
        else:
            raise ValueError(f"gpu_index must be int or list or None, not {type(gpu_index)}")
        return _str_query
    
    def _get_process_info(
        self,
        gpu_index:Union[int, list]=None,
        verbose:bool=False,
    )->list:
        outputs = subprocess.check_output(
            self._get_status_query(gpu_index=gpu_index),
            shell=True
        )
        outputs = outputs.decode('utf-8')
        if verbose:
            print(outputs)
        outputs = outputs.split('\n')[:-1]
        outputs = [output.split(',') for output in outputs]
        queries = COMPUTE_QUERY  # outputs[0]
        outputs = outputs[1:]
        
        dict_outputs = []
        for output in outputs:
            dict_output = {}
            for query, value in zip(queries, output):
                dict_output[query] = self._preprocess(query, value.strip())
            dict_outputs.append(dict_output)
        
        return dict_outputs
        
    def get(
        self,
        gpu_index:Union[int, list]=None,
        verbose:bool=False,
    )->list:
        if gpu_index == None:
            if self.count == 1:
                selected_gpu = 0
            else:
                selected_gpu = [*range(self.count)]
        elif isinstance(gpu_index, int):
            selected_gpu = gpu_index
        elif isinstance(gpu_index, list):
            if len(gpu_index) == 1:
                gpu_index = gpu_index[0]
            selected_gpu = gpu_index
        else:
            raise ValueError(f"gpu_index must be int or list or None, not {type(gpu_index)}")
        process_info = self._get_process_info(gpu_index=selected_gpu, verbose=verbose)
        len_process_info = len(process_info)
        outputs = list()
        
        for i in range(len_process_info):
            info = dict()
            gpu_index = self.uuid2index[process_info[i]['gpu_uuid']]
            for default_query in COMPUTE_QUERY:
                info[default_query] = process_info[i][default_query]
                

            info['gpu_index'] = gpu_index
            info['process_memory_total_utilization'] = 100 * info['used_gpu_memory'] / self.memory_total[gpu_index]
            info['process_memory_allocated_utilization'] = 100 * info['used_gpu_memory'] / self.memory_used[gpu_index]
            
            outputs.append(info)
        
        return outputs
    
    def _preprocess(
        self,
        query:str,
        value:str,
    )->str:
        if query == 'used_gpu_memory':
            value = value.replace('MiB', '').replace(' ', '')
            value = float(value)
            return value
        return value    
    
    def keys(
        self,
    )->list:
        query = COMPUTE_QUERY.copy()
        query.append('gpu_index')
        query.append('process_memory_total_utilization')
        query.append('process_memory_allocated_utilization')
        return query