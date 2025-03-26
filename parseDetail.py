# -*- coding: utf-8 -*-

import json
import mysql.connector
from tqdm import tqdm as tdqm

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

# 数据库连接参数
config = {
    'user': 'root',
    'password': '1234_qwer',
    'host': 'localhost',
    'database': 'mydatabase'
}


    # 查询数据库
    # 周 - 星期 - 校区 - 楼 - 节数 - 空教室列表 求并集
    # 30 * 7 * 5 * 844 * 13 

    # 临时存储处理中教室
def delete_table(cursor, db):
    cursor.execute("DROP TABLE IF EXISTS empty_classrooms")
    db.commit()
    print("删库成功")

def create_table(cursor, db):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS empty_classrooms (
        -- id INT AUTO_INCREMENT PRIMARY KEY,
        week TINYINT CHECK (week BETWEEN 1 AND 40),                 -- 周数
        day_of_week TINYINT CHECK (day_of_week BETWEEN 1 AND 7),    -- 星期，1代表周一，7代表周日
        campus VARCHAR(50) NOT NULL,                                -- 校区名称
        building VARCHAR(50) NOT NULL,                              -- 教学楼名称
        class_num TINYINT CHECK (class_num BETWEEN 1 AND 13),       -- 节数
        available_classrooms TEXT,                                  -- 空教室列表，存储为逗号分隔的教室名
        PRIMARY KEY (week, day_of_week, campus, building, class_num)
    )
    '''

    cursor.execute(create_table_query)
    db.commit()
    print("表创建成功！")

# def init_table(cursor):
#     insert_query = '''
#     INSERT INTO empty_classrooms (week, day_of_week, campus,
#                     building, time_slot, available_classrooms) 
#     VALUES (%s, %s, %s, %s, %s, %s)
#     '''
#     for week in range(1, 41):
#         for day_of_week in range(1, 8):
#             for campus in range(1, 5):
#                 # for
#                 pass

def process_classroom(rows):
    # 处理每个教室
    marks = [[[0] * 13 for _ in range(7)] for _ in range(30)]
    # 30 星期 一周 7 天 13 节
    

    for cource in rows:
        l = cource["KSJC"] # 开始节次
        r = cource["JSJC"] # 结束节次
        week = 0
        for is_class in cource["SKZC"]:
            if is_class == '1':
                for k in range(l-1, r):
                    marks[week][cource["SKXQ"]][k] = 1
            week +=1
    
    return marks

def insert_to_table(db, cursor, marks, campus, building, classroom):
    '''
    将处理好的教室数据插入到数据库
    '''
    
    insert_query = '''
    INSERT INTO empty_classrooms (week, day_of_week, campus, building, class_num, available_classrooms) 
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    available_classrooms = IFNULL(CONCAT(available_classrooms, ',', %s), %s)
    '''
    data = []
                    
    for week in range(0, len(marks)): # 周
        for day in range(0, len(marks[week])): # 星期
            for i in range(0, len(marks[week][day])): # 节数
                if marks[week][day][i] == 0:
                    data.append((week+1, day+1, campus, building, i, classroom, classroom, classroom))
    
    # data = [(1, 1, "0101", "010102", 1, "101", "101", "101")]
    # data = [(int(1), int(1), str("东院"), str("弘毅楼"), int(1), str("101"), str("101"))]

    
    # cursor.executemany(insert_query, data)
    for d in data:
        cursor.execute(insert_query, d)
    db.commit()
    
        

# cursor.executemany(insert_query, data)
# conn.commit()
# print("数据插入成功！")

def process_classrooms(cursor, db):
    '''
    读取 list.json 文件，提取教室代码，
    对所有教室进行处理，加到数据库
    '''
    with open('list.json', 'r', encoding='utf-8') as list:
        classroom_codes = json.load(list).get("datas", {}).get("jscx", {}).get("rows", []).get("JASDM")
    
    building_code_keys = building_code_to_string.keys()
    
    for code in tdqm(classroom_codes,"Processing classroom:"):
        if code[:6] not in building_code_keys:
            continue

         # 读取 JSON 文件
        with open(f"details/{code}.json", 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 提取课程数据
        rows = data.get("datas", {}).get("jaskcb", {}).get("rows", [])
        
        campus = code[:4]
        building = code[:6]
        roomcode = code[:-3]

        insert_to_table(db, cursor, process_classroom(rows), campus, building, roomcode)


def update_database():
    # 连接到 MySQL
    try:
        db = mysql.connector.connect(**config)
        print("成功连接到数据库！")
    except mysql.connector.Error as e:
        print(f"数据库连接失败：{e}")
        
    cursor = db.cursor()

    # delete_table(cursor, db)
    # create_table(cursor, db)
    
    process_classrooms(cursor, db)
    
    cursor.close()
    db.close()

    # request_list()
    