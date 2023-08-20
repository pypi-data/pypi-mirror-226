import subprocess
from .queries import STATUS_QUERY


class Status(object):
    def __init__(
        self
    ):
        self._str_query = self._get_status_query()
        
    def _get_status_query(
        self,
    )->str:
        _str_query = ','.join(STATUS_QUERY)
        _str_query = f"nvidia-smi --query-gpu={_str_query} --format=csv"
        return _str_query
    
    def get(
        self,
        verbose:bool=False
    )->list:
        outputs = subprocess.check_output(self._str_query, shell=True)
        outputs = outputs.decode('utf-8')
        if verbose:
            print(outputs)
        
        outputs = outputs.split('\n')[:-1]
        outputs = [output.split(',') for output in outputs]
        queries = STATUS_QUERY  # outputs[0]
        outputs = outputs[1:]
        
        dict_outputs = []
        for output in outputs:
            dict_output = {}
            for query, value in zip(queries, output):
                dict_output[query] = self._preprocess(query, value.strip())
            dict_outputs.append(dict_output)
        
        return dict_outputs

    def _preprocess(
        self,
        query:str,
        value:str,
    )->str:
        if query == 'index' or query == 'count' or query == 'temperature.gpu':
            return int(value)
        elif query == 'fan.speed' or query == 'utilization.gpu':
            value = value.replace('%', '').replace(' ', '0')
            value = float(value)
            return value
        elif query == 'memory.used' or query == 'memory.total' or query == 'memory.free':
            value = value.replace('MiB', '').replace(' ', '')
            value = float(value)
            return value
        elif query == 'power.draw' or query == 'power.draw.average' or query == 'power.limit' or query == 'power.max_limit':
            value = value.replace('W', '').replace(' ', '')
            value = float(value)
            return value
        return value    

    def keys(
        self,
    )->list:
        return STATUS_QUERY
    