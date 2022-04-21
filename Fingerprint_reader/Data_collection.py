#!/usr/bin/python3
import sys
sys.path.insert(0,"/home/pi/.local/lib/python3.7/site-packages")
import pymysql.cursors

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

def collect_data(student_id,enter_time):
    with connection.cursor() as cursor:
        # 現在の日付を取得
        sql = "SELECT CURDATE()+0;"
        cursor.execute(sql)
        date = cursor.fetchone()['CURDATE()+0']
        year,month,day = split_date(str(date))

        # 現在の日時を取得
        sql = "SELECT CURTIME()+0;"
        cursor.execute(sql)
        leave_time = cursor.fetchone()['CURTIME()+0']
        print(enter_time,leave_time)
        # 滞在時間を計算
        staytime = total_minutes(str(leave_time)) - total_minutes(str(enter_time))
        # 前回の滞在時間を取得
        sql = "SELECT Staytime FROM Lab_attendance_info WHERE student_id = %s AND year = %s AND month = %s AND day = %s"
        pre_staytime = cursor.execute(sql, (student_id, year, month, day))
        # 合計滞在時間をDBに登録
        total_staytime = staytime + pre_staytime
        sql = "UPDATE Lab_attendance_info SET Staytime = %s WHERE student_id = %s AND year = %s AND month = %s AND day = %s"
        cursor.execute(sql, (total_staytime, student_id, year, month, day))
        connection.commit()

        print("滞在記録を登録しました")
        cursor.close()

# 日付を分割する関数
def split_date(date): 
    year = date[-8] + date[-7] + date[-6] + date[-5]
    month = date[-4] + date[-3]
    day = date[-2] + date[-1]
    return year, month, day

# 日時を分に変換する関数
def total_minutes(time):
    hour = int(time[-5]) + 10*int(time[-6])
    minutes = int(time[-3]) + 10*int(time[-4])
    total_minutes = hour*60 + minutes
    return total_minutes
