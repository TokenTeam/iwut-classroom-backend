# 查询：校区 - 楼

from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
from os import getenv

import databaseQuery
import requestJson
import update_redis


# 数据库连接参数
mysql_config = {
    'user': getenv("MYSQL_USER"),
    'password': getenv("MYSQL_PASSWORD"),
    'host': getenv("MYSQL_HOST"),
    'database': getenv("MYSQL_DATABASE"),
}

msq = databaseQuery.mysql_connector(mysql_config)
rds = databaseQuery.redis_connector(getenv("REDIS_HOST"), getenv("REDIS_PORT"), getenv("REDIS_DB"))

app = FastAPI()

scheduler = BackgroundScheduler()
# 使用 CronTrigger 设置每天零点更新 redis
trigger = CronTrigger(hour=0, minute=0)
scheduler.add_job(update_redis.sync_mysql_to_redis, trigger)

# 在 FastAPI 启动时启动调度器
@app.on_event("startup")
async def start_scheduler():
    scheduler.start()

# 关闭时关闭调度器
@app.on_event("shutdown")
async def shutdown_scheduler():
    scheduler.shutdown()   
    rds.close()
    msq.close()


@app.get("/get_classrooms")
def get_classrooms_redis(campus_code: str, building_code: str, start_time: int, end_time: int):
    
    data = rds.redis_query(campus_code, building_code, start_time, end_time)
    
    return {"message": "ok",
            "status": 200,
            "data": data,
            }

@app.get("/get_available_buildings")
def get_available_buildings(campus_code: str, start_time: int, end_time: int):
    data = rds.redis_query_available_buildings(campus_code, start_time, end_time)
    return {"message": "ok",
            "status": 200,
            "data": data,
            }

# 模拟 Token 验证
def verify_token(token: str = Depends(lambda token: token)):
    if token != getenv("TOKEN"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# 更新全部教室的详细信息（耗时很长）
@app.post("/update-list/")
def update_list(background_tasks: BackgroundTasks, token: str = Depends(verify_token)):
    background_tasks.add_task(requestJson.get_detail)
    return {"message": "任务已开始，稍后完成"}

@app.post("/update-redis-now/")
def update_redis_now():
    update_redis.sync_mysql_to_redis()
    return {"message": "Redis 数据库已更新"}



# 在 mysql 中查找 当前周、星期、校区、楼的空教室

# 连接到 MySQL


if __name__ == "__main__":
    # print(mysql_single_query(cursor, 5, 3, "0101", "010102", 1))
    # print(redis_single_query(redis_conn, "0101", "010102", 1))
    pass
    
    
