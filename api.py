# 查询：校区 - 楼

from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status
import json
import mysql.connector
import updater

# 数据库连接参数
config = {
    'user': 'root',
    'password': '1234_qwer',
    'host': 'localhost',
    'database': 'mydatabase'
}
try:
    db = mysql.connector.connect(**config)
    print("成功连接到数据库！")
except mysql.connector.Error as e:
    print(f"数据库连接失败：{e}")
    
cursor = db.cursor()

app = FastAPI()

def single_query(cursor, week, day_of_week, campus, building, class_num):
    
    query = """
    SELECT available_classrooms
    FROM empty_classrooms
    WHERE week = %s AND day_of_week = %s AND campus = %s AND building = %s AND class_num = %s
    """
    
    cursor.execute(query, (week, day_of_week, campus, building, class_num))

    result = cursor.fetchall()
    
    return result

def query(cursor, week, day_of_week, campus, building, start_time, end_time):
    result = []
    for cl in range(start_time, end_time):
        temp = single_query(cursor, week, day_of_week, campus, building, cl)
        

    
    if len(result) == 0:
        return "无数据"
    else:
        return result[0][0]

@app.get("/get_classrooms")
async def read_root(campus_code: str, building_code: str, start_time: int, end_time: int):
    # 开始时间与结束时间都是节数
    for cl in range(start_time, end_time):
        await query(cursor, 1, 1, campus_code, building_code, cl)
    
    return {"message": "ok",
            "status": 200,
            }
    

def func():
    import time
    print("开始执行耗时任务...")
    time.sleep(30)  # 模拟耗时30秒
    print("任务完成！")

# 模拟 Token 验证
def verify_token(token: str = Depends(lambda token: token)):
    if token != "your_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# 更新列表的接口
@app.post("/update-list/")
def update_list(background_tasks: BackgroundTasks, token: str = Depends(verify_token)):
    background_tasks.add_task(updater.update)
    return {"message": "任务已开始，稍后完成"}


# 在 mysql 中查找 当前周、星期、校区、楼的空教室

# 连接到 MySQL


if __name__ == "__main__":
    single_query(cursor, 1, 1, "东院", "弘毅楼(附楼)", 1)

