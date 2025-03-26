import mysql.connector
import redis

class mysql_connector:
    def __init__(self, config):
        self.config = config
        self.cursor = None
        self.db = None
        self.connect_mysql()
        
    def connect_mysql(self):
        try:
            self.db = mysql.connector.connect(**self.config)
            print("成功连接到mysql！")
        except mysql.connector.Error as e:
            print(f"mysql连接失败：{e}")
            exit(1)
        
        self.cursor = self.db.cursor()
        
    def mysql_single_query(self, week, day_of_week, campus, building, class_num):
        
        query = """
        SELECT available_classrooms
        FROM empty_classrooms
        WHERE week = %s AND day_of_week = %s AND campus = %s AND building = %s AND class_num = %s
        """
        
        self.cursor.execute(query, (week, day_of_week, campus, building, class_num))

        result = self.cursor.fetchone()[0].split(",")
        
        # result.sort()
        
        return set(result)

    def mysql_query(self, week, day_of_week, campus, building, start_time, end_time):
        result = {}
        for cl in range(start_time, end_time):
            if len(result) == 0:
                result = self.mysql_single_query(week, day_of_week, campus, building, cl)
                continue
            
            temp = self.mysql_single_query(week, day_of_week, campus, building, cl)
            result = result & temp
            
        return sorted(list(result))
    
    def close(self):
        self.cursor.close()
        self.db.close()

class redis_connector:
    def __init__(self, host, port, db):
        self.redis_conn = None
        self.host = host
        self.port = port
        self.db = db
        
        self.connect()
        
        
    def connect(self):
        try:
            self.redis_conn = redis.Redis(host=self.host, port=self.port, db=self.db)
            print("成功连接到redis！")
        except mysql.connector.Error as e:
            print(f"redis连接失败：{e}")
            exit(1)

    def redis_single_query(self, campus, building, class_num):
        key = f"{campus},{building},{class_num}"
        return set(self.redis_conn.get(key).decode().split(","))

    def redis_query(self, campus, building, start_time, end_time):   
        result = {}
        for cl in range(start_time, end_time + 1):
            if len(result) == 0:
                result = self.redis_single_query(campus, building, cl)
                continue
            
            temp = self.redis_single_query(campus, building, cl)
            result = result & temp
            
        return sorted(list(result))
    
    def close(self):
        self.redis_conn.close()
    

if __name__ == '__main__':
    rds = redis_connector('localhost', 6379, 0)
    
    print(rds.redis_query("0101", "010102", 1, 9))
    
    rds.close()