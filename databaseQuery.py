import mysql.connector
import redis


building_code_to_string = {
    "010102": "弘毅楼(附楼)",
    "010103": "弘毅楼(主楼)",
    "010106": "致远楼",

    "010201": "东教学楼",

    "020101": "爱特楼",
    "020102": "北教一",
    "020103": "北教二",
    "020104": "北教三",
    "020105": "学海楼",

    "020201": "博学北楼",
    "020202": "博学东楼",
    "020203": "博学西楼",
    "020204": "博学主楼",

    "030102": "教学大楼",
    "030201": "航海楼",
}

# 0101xx 东院
# 0102xx 西院
# 0201xx 鉴湖
# 0202xx 南湖
# 03xxxx 余区
building_code_to_campus = {
    "0101": "东院",
    "0102": "西院",
    "0201": "鉴湖校区",
    "0202": "南湖校区",
    "0301": "余家头校区",
    "0302": "余家头校区",
}

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
        result = self.redis_conn.get(key)
        if result is None:
            # 处理未找到数据的情况
            return set()
        return set(result.decode().split(","))

        # return set(self.redis_conn.get(key).decode().split(","))

    def redis_query(self, campus, building, start_time, end_time):   
        result = {}
        for cl in range(start_time, end_time + 1):
            if len(result) == 0:
                result = self.redis_single_query(campus, building, cl)
                continue
            
            temp = self.redis_single_query(campus, building, cl)
            result = result & temp
            
        return sorted(list(result))
    
    def redis_query_available_buildings(self, campus, start_time, end_time):
        result = []
        for building in building_code_to_string.keys():
            if building[:4] != campus:
                continue

            for cl in range(start_time, end_time + 1):
                temp = self.redis_single_query(campus, building, cl)
                if len(temp) > 0:
                    result.append(building)
                    break
        
        return result

    
    def close(self):
        self.redis_conn.close()
    

if __name__ == '__main__':
    rds = redis_connector('localhost', 6379, 0)
    
    print(rds.redis_query("0101", "010102", 1, 9))
    
    rds.close()