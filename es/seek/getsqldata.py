import pymysql
from time import sleep

from seek import setting
from seek import participle

class OperationMysql(object):
    def __init__(self):
        self.sql = "select * from datainfo"

    def getData(self):
        '''
        从数据库中获取每一条数据
        :return:
        '''
        try:
            # 连接数据库
            connection = pymysql.connect(**setting.Config)
            # 用流式游标进行操作数据库
            with connection.cursor(pymysql.cursors.SSCursor) as cursor:
                # 执行sql语句
                cursor.execute(self.sql)
                while True:
                    # 每次获取一条数据
                    result = cursor.fetchone()
                    if not result:
                        break
                    with open('2.txt', 'a') as f:
                        for this in result:
                            f.write(this)
                            f.write('\n\n\n\n')
                    # participle.save_es(result)
                    break

        except Exception as e:
            print(e)
        finally:
            connection.close()


if __name__ == '__main__':
    Om = OperationMysql()
    Om.getData()


