# 查询：校区 - 楼

from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status
import json

import updater

import databaseQuery


# 数据库连接参数
config = {
    'user': 'root',
    'password': '1234_qwer',
    'host': 'localhost',
    'database': 'mydatabase'
}

msq = databaseQuery.mysql_connector(config)
rds = databaseQuery.redis_connector('localhost', 6379, 0)

app = FastAPI()


@app.get("/get_classrooms")
def get_classrooms_redis(campus_code: str, building_code: str, start_time: int, end_time: int):
    
    data = rds.redis_query(campus_code, building_code, start_time, end_time)
    
    return {"message": "ok",
            "status": 200,
            "data": data,
            }


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
    # print(mysql_single_query(cursor, 5, 3, "0101", "010102", 1))
    # print(redis_single_query(redis_conn, "0101", "010102", 1))
    pass
    
    
rds.close()
msq.close()
