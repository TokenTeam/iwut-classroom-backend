# -*- coding: utf-8 -*-

'''
初始化数据库并写入空教室数据
1. 连接 MySQL，建表
2. 读取 list.json + details/*.json，解析并写入
'''

import json
import mysql.connector
from os import getenv
from tqdm import tqdm

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

config = {
    'user': getenv("MYSQL_USER") or 'root',
    'password': getenv("MYSQL_PASSWORD") or '123456',
    'host': getenv("MYSQL_HOST") or 'localhost',
    'database': getenv("MYSQL_DATABASE") or 'classrooms',
}


def connect():
    db = mysql.connector.connect(**config)
    print("成功连接到数据库")
    return db, db.cursor()


def create_table(cursor, db):
    cursor.execute("DROP TABLE IF EXISTS empty_classrooms")
    cursor.execute('''
        CREATE TABLE empty_classrooms (
            week TINYINT CHECK (week BETWEEN 1 AND 40),
            day_of_week TINYINT CHECK (day_of_week BETWEEN 1 AND 7),
            campus VARCHAR(50) NOT NULL,
            building VARCHAR(50) NOT NULL,
            class_num TINYINT CHECK (class_num BETWEEN 1 AND 16),
            available_classrooms TEXT,
            PRIMARY KEY (week, day_of_week, campus, building, class_num)
        )
    ''')
    db.commit()
    print("建表完成")


def process_classroom(rows):
    """解析课程数据，返回 40周x7天x16节 的占用矩阵（内部编号含中课6-7和晚课13）"""
    marks = [[[0] * 16 for _ in range(7)] for _ in range(40)]
    for course in rows:
        l = course["KSJC"]
        r = course["JSJC"]
        skxq = course["SKXQ"]
        week = 0
        for is_class in course["SKZC"]:
            if is_class == '1':
                if week >= 40 or skxq < 1 or skxq > 7 or l < 1 or r > 16:
                    print(f"  越界: week={week} SKXQ={skxq} KSJC={l} JSJC={r} SKZC长度={len(course['SKZC'])}")
                    break
                for k in range(l - 1, r):
                    marks[week][skxq - 1][k] = 1
            week += 1
    return marks


def insert_to_table(db, cursor, marks, campus, building, classroom):
    """将空闲时段插入数据库"""
    insert_query = '''
        INSERT INTO empty_classrooms (week, day_of_week, campus, building, class_num, available_classrooms)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        available_classrooms = CONCAT(available_classrooms, ',', %s)
    '''
    for week in range(len(marks)):
        for day in range(len(marks[week])):
            for i in range(len(marks[week][day])):
                if marks[week][day][i] == 0:
                    cursor.execute(insert_query, (
                        week + 1, day + 1, campus, building, i + 1,
                        classroom, classroom
                    ))
    db.commit()


def process_all():
    """读取 list.json，逐个处理教室并写入数据库"""
    db, cursor = connect()
    create_table(cursor, db)

    with open('list.json', 'r', encoding='utf-8') as f:
        classroom_rows = json.load(f).get("datas", {}).get("jscx", {}).get("rows", [])

    building_keys = building_code_to_string.keys()

    for row in tqdm(classroom_rows, desc="写入数据库"):
        code = row.get("JASDM", "")
        if code[:6] not in building_keys:
            continue

        try:
            with open(f"details/{code}.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"跳过 {code}，文件不存在")
            continue

        rows = data.get("datas", {}).get("jaskcb", {}).get("rows", [])
        print(f"\n处理 {code}，共 {len(rows)} 条课程")
        marks = process_classroom(rows)
        insert_to_table(db, cursor, marks, code[:4], code[:6], code[-3:])

    cursor.close()
    db.close()
    print("全部写入完成")


if __name__ == '__main__':
    process_all()
