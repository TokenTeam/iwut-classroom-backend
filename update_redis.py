import mysql.connector
import redis
from datetime import datetime
import datetime

start_date = datetime.date(2025, 2, 24)

mysql_config = {
    'user': 'root',
    'password': '1234_qwer',
    'host': 'localhost',
    'database': 'mydatabase'
}

# 配置 MySQL 连接
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# 配置 Redis 连接
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

def clear_redis():
    redis_conn.flushdb()
    print("已清空 Redis 数据库！")

# 每天执行的任务
def sync_mysql_to_redis():
    query = """
    SELECT *
    FROM empty_classrooms
    WHERE week = %s AND day_of_week = %s 
    """
    
    # 获取今天的日期
    today = datetime.date.today()
    # 计算今天距离 2月24日 的天数差
    days_diff = (today - start_date).days
    # 计算当前是第几周
    week_number = days_diff // 7 + 1  # 每 7 天为一周
    # 计算今天是星期几 (1=星期一，...，7=星期日)
    weekday = today.weekday() + 1  # 加 1，使得 0 = 星期一，7 = 星期日
    
    mysql_cursor.execute(query, (week_number, weekday))
    data = mysql_cursor.fetchall()
    
    pipe = redis_conn.pipeline()
    
    for row in data:
        # print(row)
        # break
        key = f"{row[2]},{row[3]},{row[4]}"  # 校区号,教学楼号,第几节课
        pipe.set(key, row[5])  # 空闲教室
    pipe.execute()
    print("同步成功！") 
    

if __name__ == "__main__":
    clear_redis()

    # 调用函数进行同步
    sync_mysql_to_redis()

    # 关闭数据库连接ff
    mysql_cursor.close()
    mysql_conn.close()

    redis_conn.close()

