:
        db = mysql.connector.connect(**config)
        print("成功连接到数据库！")
    except mysql.connector.Error as e:
        print(f"数据库连接失败：{e}")
        exit(1)
        
    cursor = db.cursor()

    delete_table(cursor, db)
    create_table(cursor, db)
    
    process_classrooms(cursor, db)
    
    cursor.close()
    db.close()