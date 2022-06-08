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

def collect_data(student_id):
    with connection.cursor() as cursor:
        # 現在の日付を取得
        sql = "SELECT CURDATE();"
        cursor.execute(sql)
        date = cursor.fetchone()['CURDATE()']

        # 現在の日時を取得
        sql = "SELECT CURTIME();"
        cursor.execute(sql)
        enter_time = cursor.fetchone()['CURTIME()']

        try:
            # 今日が初めての入室ならエラー、except文へ
            sql = "SELECT student_id FROM Lab_report WHERE student_id = %s  AND date = %s"
            cursor.execute(sql, (student_id, date))
            anything = cursor.fetchone()['student_id']
            
            cursor.close()

        except:
            # 今日が初めての入室ならDBに入室時刻を登録
            sql = "INSERT INTO Lab_report VALUES(%s,%s,%s,%s,%s);"
            cursor.execute(sql,(student_id, date, enter_time, 0, None))
            connection.commit()
            cursor.close()

def get_tmptime(student_id):
    with connection.cursor() as cursor:
        # update_timeをtmp_timeとして取得
        sql = "SELECT DATE_FORMAT(update_time, %s) AS update_time FROM Lab_attendance_tb WHERE user_id = %s"
        cursor.execute(sql, ('%H%i%s', student_id))
        tmp_time = cursor.fetchone()['update_time']
        
        return tmp_time

def calc_staytime(student_id,tmp_time):
    with connection.cursor() as cursor:
        # 退室、一時退室時に実行
        #更新前(入室時間)を更新時間(退室時間)から引く
        # 現在の日時を取得
        sql = "SELECT CURTIME()+0;"
        cursor.execute(sql)
        leave_time = cursor.fetchone()['CURTIME()+0']

        staytime = total_minutes(str(leave_time)) - total_minutes(tmp_time)

        # staytimeを更新

        # 現在の日付を取得(更新のwhere条件に必要なので)
        sql = "SELECT CURDATE();"
        cursor.execute(sql)
        date = cursor.fetchone()['CURDATE()']

        # 今までのstaytimeを取得(初めての退室なら0)
        sql = "SELECT staytime FROM Lab_report WHERE student_id = %s  AND date = %s"
        cursor.execute(sql, (student_id, date))
        before_staytime = cursor.fetchone()['staytime']

        # 計算したstaytimeを合算
        now_staytime = before_staytime + staytime
    
        # データを更新
        sql = "UPDATE Lab_report SET staytime = %s WHERE student_id = %s AND date = %s"
        cursor.execute(sql, (now_staytime, student_id, date))
        connection.commit()

        cursor.close()

def total_minutes(time):
    hour = int(time[-5]) + 10*int(time[-6])
    minutes = int(time[-3]) + 10*int(time[-4])
    total_minutes = hour*60 + minutes

    return total_minutes
    