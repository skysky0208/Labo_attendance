#!/usr/bin/python3
import sys
sys.path.insert(0,"/home/pi/.local/lib/python3.7/site-packages")
import pymysql.cursors
import play


# Connect to the database
# データベースに接続
connection = pymysql.connect(host='127.0.0.1', # Raspberry PiのIPアドレスではないので注意
                             port=3306, # ポート番号
                             user='root', # ユーザー名
                             passwd='admin', # パスワード
                             db='Lab_attendance', # データベース名
                             charset='utf8mb4', # 文字コード 
                             cursorclass=pymysql.cursors.DictCursor, # 結果をdictで受け取る 
                             autocommit=False) # オートコミットの設定
                    
def convert_data(positionNumber):
    with connection.cursor() as cursor:
        # student_idを探索
        sql = "SELECT user_id FROM Lab_fingerprint_tb WHERE finger_id = %s"
        # student_idを取得
        cursor.execute(sql, positionNumber)
        student_id = cursor.fetchone()['user_id']

        if student_id is None:
            print("Error:Unregistered data")
            play.playerrorsound()
            
        cursor.close()
        return student_id