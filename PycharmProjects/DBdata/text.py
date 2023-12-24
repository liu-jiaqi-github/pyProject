import cx_Oracle

# 设置链接参数
user_name = 'JCZT'
password = 'JCZT'
connect_str = '192.168.137.2:1521/helowin'

# 先建立连接
conn = cx_Oracle.connect(user_name, password, connect_str)

# 如果使用着这种报错的话需使用以下方式, 报错: ORA-12154: TNS: 无法解析指定的连接标识符
#conn = cx_Oracle.connect(user_name, password, cx_Oracle.makedsn('192.168.137.2', '1521', None, 'helowin'))

# 定义游标
cursor = conn.cursor()
# 定义sql
sql = 'select* from BIP_DATA_ENTITY_MGR'
# 向数据库发送sql
cursor.execute(sql)
# 获取数据, fetchall()获取全部数据
results = cursor.fetchall()
# 获取字段名称
fields = [field[0] for field in cursor.description]
# print(fields)
# 把数据与字段关连起来
res = [dict(zip(fields, result)) for result in results]

# 从数据列表中取出每段数据
for rlt in res:
    print(rlt)
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
