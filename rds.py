import mysql.connector
from mysql.connector import Error

def connectDB():
    conn = mysql.connector.connect(
        host='',  
        user='',  # 데이터베이스 사용자 이름
        password='',  # 데이터베이스 비밀번호
        database=''  # 연결할 데이터베이스 이름
    )
    return conn


# select
def getEnteranceUser():
    
    try:

        conn = connectDB()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM user ORDER BY time DESC LIMIT 1"

        cursor.execute(sql)
        [result] = cursor.fetchall()
        
    except Exception as e:
        print("getOrder에서 오류 발생", e)
    finally:
        cursor.close()
        conn.close()

    return result

