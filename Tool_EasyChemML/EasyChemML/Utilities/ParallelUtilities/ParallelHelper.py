from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Manager
from tqdm import tqdm
import numpy as np, os, time
from concurrent.futures import ProcessPoolExecutor

from EasyChemML.Utilities.ParallelUtilities.IndexQueues.IndexQueue_Inorder import IndexQueue_Inorder
from EasyChemML.Utilities.ParallelUtilities.IndexQueues.IndexQueue_settings import IndexQueue_settings
from EasyChemML.Utilities.ParallelUtilities.Shared_PythonList import Shared_PythonList

"""
Typing section
https://pypi.org/project/loky/
"""
from typing import Dict, Tuple, List


class ParallelHelper():
    _processPool: ProcessPoolExecutor
    _max_worker: int

    def __init__(self, n_jobs: int):
        self._processPool, self._max_worker = self._createProcessPoolExecutor(n_jobs)

    def _createProcessPoolExecutor(self, n_jobs):
        if n_jobs == -1:
            n_jobs = os.cpu_count()
        elif n_jobs < -1:
            n_jobs = os.cpu_count() + (n_jobs+1)
        elif n_jobs == 0:
            raise Exception(f'n_jobs is 0')

        if n_jobs > 61:
            if os.name == 'nt':
                print('!!! on Windows the maximum n_jobs is 61 !!!')
                print('!!! n_jobs is set to 61 !!!')
                n_jobs = 61

        print(f'ProcessPool is alive')
        return ProcessPoolExecutor(n_jobs), n_jobs

    def __del__(self):
        self._processPool.shutdown(wait=True)
        self._processPool.shutdown(wait=True)
        print(f'ProcessPool is shutdown')

    @staticmethod
    def _closeSharedMem(kwargs):
        for key in kwargs:
            if isinstance(kwargs[key], Shared_PythonList):
                kwargs[key].close()


    @staticmethod
    def _parallelExecuter_MAP_orderd_return(out_dtypes, indexqueue: IndexQueue_Inorder, function,
                                     **kwargs):
        kwargs['out_dtypes'] = out_dtypes
        out_array = np.empty(shape=(indexqueue.itemCount,), dtype=out_dtypes)
        out_array_pointer = 0
        for chunk in indexqueue:
            chunk = list(chunk)
            kwargs['current_chunk'] = chunk
            result = function(**kwargs)
            out_array[out_array_pointer:out_array_pointer+len(chunk)] = result
            out_array_pointer += len(chunk)
        ParallelHelper._closeSharedMem(kwargs)
        return out_array

    def execute_map_orderd_return(self, fn, IQ_settings: IndexQueue_settings, out_dtypes, **kwargs):
        #TODO add/create non Process executing when n_jobs = 1

        jobs = []
        m = Manager()
        for i in range(self._max_worker):
            new_indexqu = IndexQueue_Inorder(IQ_settings, i, self._max_worker, m)
            j = self._processPool.submit(ParallelHelper._parallelExecuter_MAP_orderd_return, out_dtypes,
                                         new_indexqu, fn, **kwargs)
            jobs.append((j, new_indexqu))

        with tqdm(total=len(IQ_settings)) as pbar:
            finished = False
            while not finished:
                finished = True
                status_count = 0
                for job, handler in jobs:
                    handler_val = handler.get_already_processed()
                    status_count += handler_val
                    if not job.done():
                        finished = False
                if not pbar.n == status_count:
                    pbar.n = status_count
                    pbar.refresh()
                time.sleep(0.1)

        for _, handler in jobs:
            handler.reset_closeShared()

        out_array = np.empty(shape=(len(IQ_settings),), dtype=out_dtypes)

        for job, handler in jobs:
            job_pointer = 0
            job_result = job.result()
            for chunk in handler:
                out_array[chunk] = job_result[job_pointer:job_pointer+len(chunk)]
                job_pointer += len(chunk)
        m.shutdown()
        return out_array
