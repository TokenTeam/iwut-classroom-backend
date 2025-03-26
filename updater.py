import requestJson
import parseDetail

def update():
    print("开始更新列表...")
    requestJson.get_detail()
    print("更新列表完成！")
    
    print("开始更新教室数据...")
    parseDetail.update_database()
    print("更新教室数据完成！")