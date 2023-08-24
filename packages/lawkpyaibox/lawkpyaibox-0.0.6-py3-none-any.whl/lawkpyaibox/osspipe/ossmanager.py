import oss2


class OSSManager:

    def __init__(
        self,
        oss_key="",
        oss_secret="",
        oss_endpoint="http://oss-cn-hangzhou.aliyuncs.com",
        oss_bucketname="",
    ):
        self.auth = oss2.Auth(oss_key, oss_secret)
        self.oss_endpoint = oss_endpoint
        self.oss_bucket = oss2.Bucket(self.auth, self.oss_endpoint,
                                      oss_bucketname)

    def reset_ossbucket(self, oss_bucketname):
        self.oss_bucket = oss2.Bucket(self.auth, self.oss_endpoint,
                                      oss_bucketname)

    def list_oss_path(self, oss_path, file_postfix):
        filelst = []
        for obj in oss2.ObjectIterator(self.oss_bucket,
                                       delimiter='/',
                                       prefix=oss_path):
            if obj.is_prefix():
                filelst_sub = self.list_oss_path(str(obj.key), file_postfix)
                for file in filelst_sub:
                    filelst.append(file)
            else:
                if str(obj.key).endswith(file_postfix):
                    filelst.append(str(obj.key))
        return filelst

    def parse_oss_path(self, osspath_lst, osspath_prex, file_postfix):
        ossfilelst = []
        for osspath in osspath_lst:
            lstitem = self.list_oss_path(osspath_prex + osspath + '/',
                                         file_postfix)
            for item in lstitem:
                ossfilelst.append(item)
        return ossfilelst

    def download_file_from_oss(self, file_osspath, file_localpath):
        try:
            self.oss_bucket.get_object_to_file(file_osspath, file_localpath)
            return True
        except:
            print("download {} failed".format(file_osspath))
            return False

    def push_file_to_oss(self, file_localpath, file_osspath):
        self.oss_bucket.put_object_from_file(file_osspath, file_localpath)

    def list_ossdir_iterwalk(self, ossprefix):
        result_file_list = []
        for obj in oss2.ObjectIteratorV2(self.oss_bucket, prefix=ossprefix):
            result_file_list.append(obj.key)
        return result_file_list

    def oss_search_target_ext_file(self, ossprefix, target_ext=".txt"):
        result_file_list = []
        for obj in oss2.ObjectIteratorV2(self.oss_bucket, prefix=ossprefix):
            if target_ext in obj.key:
                result_file_list.append(obj.key)
        return result_file_list

    def list_ossdir(self, ossprefix):
        result_file_list = []
        for obj in oss2.ObjectIterator(self.oss_bucket,
                                       delimiter='/',
                                       prefix=ossprefix):
            result_file_list.append(obj.key)
        return result_file_list
