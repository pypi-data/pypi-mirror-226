import threading
import os
import time
from pyaibox.osspipe import ossmanager


class ServiceBoardX(object):

    def __init__(self,
                 logfilepath=None,
                 update_timer=0,
                 max_lifecircle=3600,
                 oss_key="",
                 oss_secret="",
                 oss_endpoint="",
                 oss_bucket="",
                 upload_bucket_subdir=""):
        """

        Args:
            logfilepath ([type], optional): [description]. Defaults to None.
            update_timer (int, optional): [description]. Defaults to 0.
            max_lifecircle (int, optional): max service running time [second]
        """
        self.logfile = None
        self.logfilepath = logfilepath
        if self.logfilepath is not None:
            self.logfile = open(logfilepath, 'w')
        self.update_timer = update_timer
        self.logupdate_timer = None
        if self.update_timer > 0:
            self.logupdate_timer = threading.Timer((5, self.run_timer_func))
            self.logupdate_timer.start()
        self.service_st = time.time()
        self.is_boarder_active = True
        self.max_lifecircle = max_lifecircle
        self.ossmanager = None
        self.upload_bucket_subdir = upload_bucket_subdir
        if oss_key != "":
            self.ossmanager = ossmanager.OSSManager(oss_key=oss_key,
                                                    oss_secret=oss_secret,
                                                    oss_endpoint=oss_endpoint,
                                                    oss_bucket=oss_bucket)

    def get_ossmanager(self):
        return self.ossmanager

    def run_timer_func(self):
        service_et = time.time()
        durtime = service_et - self.service_st
        print("serviceBoardX running time: {:.6}s".format(durtime))
        if self.logfile is not None:
            self.logfile.flush()

        if durtime > self.max_lifecircle:
            self.release()

        if self.logfilepath is not None and os.path.existsself.logfilepath:
            remotepath = "{}/{}".format(self.upload_bucket_subdir,
                                        os.path.basename(self.logfilepath))
            if self.ossmanager is not None:
                self.ossmanager.push_file_to_oss(self.logfilepath, remotepath)

        if self.is_boarder_active and self.logupdate_timer is not None:
            self.logupdate_timer = threading.Timer(self.update_timer,
                                                   self.run_timer_func)
            self.logupdate_timer.start()

    def loginfo(self, logstr):
        print(logstr)
        if self.logfile is not None:
            print(logstr, file=self.logfile)

    def show_progress(self, curridx, endidx, headerstr=""):
        self.loginfo("{}, progress: {}/{}, {:.2f}%".format(
            headerstr, curridx, endidx, curridx / endidx * 100))

    def show_progress_time(self,
                           threadid,
                           thread_et,
                           thread_st,
                           curridx,
                           endidx,
                           headerstr=""):
        if curridx == 0:
            print("Threadid {}, {} process progress {}/{}, {:.4f}%".format(
                threadid, headerstr, curridx, endidx, curridx / endidx * 100))
            return

        remain_time = int(
            (thread_et - thread_st) / curridx * (endidx - curridx))
        cost_time = int(thread_et - thread_st)
        timeinfo = "{}:{:02}:{:02}<{}:{:02}:{:02}".format(
            cost_time // 3600, cost_time % 3600 // 60, cost_time % 60,
            remain_time // 3600, remain_time % 3600 // 60, remain_time % 60)
        self.loginfo(
            "Threadid {}, {} process progress: {}/{}, {:.4f}%, [{}]".format(
                threadid, headerstr, curridx, endidx, curridx / endidx * 100,
                timeinfo))

    def release(self):
        self.loginfo("Release timer and service boarder!")
        if self.logupdate_timer is not None:
            self.logupdate_timer.join()
        self.is_boarder_active = False
        if self.logfile is not None:
            self.logfile.close()
            self.logfile = None
