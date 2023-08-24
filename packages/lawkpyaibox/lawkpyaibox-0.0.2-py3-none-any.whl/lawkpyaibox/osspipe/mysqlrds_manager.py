import pymysql


class MysqlRdsManager():

    def __init__(self,
                 host='',
                 user="",
                 password="",
                 schema_database='',
                 use_longconn=False):
        self.mysql_host = host
        self.mysql_user = user
        self.mysql_password = password
        self.schema_database = schema_database
        self.mysql_charset = 'utf8'
        self.conn = None
        self.cursor = None
        if use_longconn:
            self.conn = pymysql.connect(host=self.mysql_host,
                                        user=self.mysql_user,
                                        password=self.mysql_password,
                                        database=self.schema_database,
                                        charset=self.mysql_charset)
            print('连接数据库成功！')
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def query(self, querycmd, values=None):
        results, status = "None", 0
        if self.conn is None:
            try:
                self.conn = pymysql.connect(host=self.mysql_host,
                                            user=self.mysql_user,
                                            password=self.mysql_password,
                                            database=self.schema_database,
                                            charset=self.mysql_charset)
                self.cursor = self.conn.cursor(
                    cursor=pymysql.cursors.DictCursor)
                # print("MySQL connect successfully!")
            except Exception as e:
                print("MySQL-RDS connection error, code: {} ".format(e))
                status = 502
                return "None", status

        try:
            # 提交到数据库执行
            if values is None:
                self.cursor.execute(querycmd)
            else:
                self.cursor.execute(querycmd, values)
            self.conn.commit()
            results = self.cursor.fetchall()
            # print("Query execute done, results:{}".format(results))

        except Exception as e:
            print("MySQL-RDS query error, code: {} ".format(e))
            status = 503

        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        self.conn = None
        # print("MySQL close connect finished!")

        return results, status

    def __del__(self):
        # close
        if self.conn is not None:
            print("\nAuto delete connect with rds-mysql-database!")
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
