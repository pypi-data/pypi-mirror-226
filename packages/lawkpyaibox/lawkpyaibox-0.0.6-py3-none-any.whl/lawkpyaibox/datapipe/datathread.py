import time
from threading import Thread
from multiprocessing import Process


class ThreadFunc(object):
    """Thread Function
    """

    def __init__(self, func, loopname, **kwargs):
        self.func = func
        self.loopname = loopname
        self.kwargs = kwargs

    def __call__(self):
        self.func(self.loopname, **self.kwargs)


class ProcessDataFunc(ThreadFunc):

    def __init__(self, func, loopname, datalst, **kwargs):
        """
        Args:
            func ([function]): thread process func
            loopname ([int]): thread idx
            datalst ([list]): dataset
        """
        super().__init__(func, loopname, **kwargs)
        self.func = func
        self.loopname = loopname
        self.datalst = datalst
        self.kwargs = kwargs

    def __call__(self):
        self.func(self.loopname, self.datalst, **self.kwargs)


def multiprocess_data_interpreter(thread_runner_func, thread_num, datalst,
                                  **kwargs):
    print("*" * 60)
    threads = []
    splitnum = len(datalst) // thread_num
    for thidx in range(thread_num):
        data_startidx = thidx * splitnum
        data_endidx = len(datalst)
        if thidx < (thread_num - 1):
            data_endidx = (thidx + 1) * splitnum
        mp = Process(target=thread_runner_func,
                     args=(thidx, datalst[data_startidx:data_endidx]),
                     kwargs=kwargs)
        threads.append(mp)

    for i in range(thread_num):
        threads[i].start()
        time.sleep(0.001)

    for i in range(thread_num):
        threads[i].join()

    print("Finish multiprocess_data_interpreter")
    print("*" * 60)


def multithread_data_interpreter(thread_runner_func, thread_num, datalst,
                                 **kwargs):
    print("*" * 60)
    threads = []
    splitnum = len(datalst) // thread_num
    for thidx in range(thread_num):
        data_startidx = thidx * splitnum
        data_endidx = len(datalst)
        if thidx < (thread_num - 1):
            data_endidx = (thidx + 1) * splitnum
        thread = Thread(
            target=ThreadFunc(thread_runner_func,
                              thidx,
                              datalst=datalst[data_startidx:data_endidx],
                              **kwargs))
        threads.append(thread)

    for i in range(thread_num):
        threads[i].start()
        time.sleep(0.001)

    for i in range(thread_num):
        threads[i].join()

    print("Finish multithread_data_interpreter")
    print("*" * 60)


def thread_show_progress(threadid,
                         thread_et,
                         thread_st,
                         curridx,
                         endidx,
                         headerstr=""):
    if curridx == 0:
        print("Threadid {}, {} process progress {}/{}, {:.4f}%".format(
            threadid, headerstr, curridx, endidx, curridx / endidx * 100))
        return

    remain_time = int((thread_et - thread_st) / curridx * (endidx - curridx))
    cost_time = int(thread_et - thread_st)
    timeinfo = "{}:{:02}:{:02}<{}:{:02}:{:02}".format(
        cost_time // 3600, cost_time % 3600 // 60, cost_time % 60,
        remain_time // 3600, remain_time % 3600 // 60, remain_time % 60)
    print("Threadid {}, {} process progress: {}/{}, {:.4f}%, [{}]".format(
        threadid, headerstr, curridx, endidx, curridx / endidx * 100,
        timeinfo))
