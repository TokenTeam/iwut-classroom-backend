# -*- coding: utf-8 -*-

import json
import mysql.connector

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

# 数据库连接参数
config = {
    'user': 'root',
    'password': '1234_qwer',
    'host': 'localhost',
    'database': 'mydatabase'
}

# 连接到 MySQL
try:
    conn = mysql.connector.connect(**config)
    print("成功连接到数据库！")
except mysql.connector.Error as e:
    print(f"数据库连接失败：{e}")

# 读取 JSON 文件
with open('detail.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 提取课程数据
rows = data.get("datas", {}).get("jaskcb", {}).get("rows", [])


# 查询数据库
# 周 - 星期 - 校区 - 楼 - 节数 - 空教室列表 求并集
# 30 * 7 * 5 * 844 * 13 

# 临时存储处理中教室

cursor = conn.cursor()

def create_table(cursor):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS empty_classrooms (
        -- id INT AUTO_INCREMENT PRIMARY KEY,
        week TINYINT CHECK (week BETWEEN 1 AND 40),                 -- 周数
        day_of_week TINYINT CHECK (day_of_week BETWEEN 1 AND 7),    -- 星期，1代表周一，7代表周日
        campus VARCHAR(50) NOT NULL,                                -- 校区名称
        building VARCHAR(50) NOT NULL,                              -- 教学楼名称
        class_num TINYINT CHECK (class_num BETWEEN 1 AND 13),       -- 节数
        available_classrooms TEXT,                                  -- 空教室列表，存储为逗号分隔的教室名
        PRIMARY KEY (week, day_of_week, campus, building, time_slot)
    )
    '''

    cursor.execute(create_table_query)
    print("表创建成功！")

def init_table(cursor):
    insert_query = '''
    INSERT INTO empty_classrooms (week, day_of_week, campus,
                    building, time_slot, available_classrooms) 
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    for week in range(1, 41):
        for day_of_week in range(1, 8):
            for campus in range(1, 5):
                # for
                pass

# data = []

marks = [[[0] * 13] * 7] * 30    # 30 星期 一周 7 天 13 节

for cource in rows:
    l = cource["KSJC"] # 开始节次
    r = cource["JSJC"] # 结束节次
    week = 0
    for is_class in cource["SKZC"]:
        if is_class is '1':
            for k in range(l-1, r):
                marks[week][cource["SKXQ"]][k] = 1
        week +=1

    

# cursor.executemany(insert_query, data)
# conn.commit()
# print("数据插入成功！")





# # 遍历并解析课程信息
# for course in rows:
#     print(f"课程名称: {course.get('KCM', '无')}")
#     print(f"授课教师: {course.get('SKJS', '无')}")
#     print(f"学分: {course.get('XF', '无')}")
#     print(f"上课时间地点: {course.get('YPSJDD', '无')}")
#     print(f"周次信息: {course.get('ZCMC', '无')}")
#     print(f"授课班级: {course.get('SKBJ', '无')}")
#     print('-' * 40)

