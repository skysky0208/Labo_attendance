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
               
def check_timeout(c_type):
    with connection.cursor() as cursor:
        if c_type =='EXIT_CARD':
            # 日時更新
            sql = "UPDATE Lab_attendance_tb SET update_time = CAST(NOW() as DATETIME) WHERE user_id = %s"
            cursor.execute(sql, 31114153)
            connection.commit()
            timeout_count = 0
        else:
            # update_timeを取得
            sql = "SELECT DATE_FORMAT(update_time, %s) AS update_time FROM Lab_attendance_tb WHERE user_id = %s"
            cursor.execute(sql, ('%H%i%s',31114153))
            update_time = cursor.fetchone()['update_time']

            # 日時更新
            sql = "UPDATE Lab_attendance_tb SET update_time = CAST(NOW() as DATETIME) WHERE user_id = %s"
            cursor.execute(sql, 31114153)
            connection.commit()

            # 現在日時を取得
            sql = "SELECT CURTIME()+0;"
            cursor.execute(sql)
            now_time = cursor.fetchone()['CURTIME()+0']

            cursor.close()

            # 現在日時と最終更新日時を比較
            # 日時を秒に変換
            update_time_second = total_second(update_time)
            now_time_second = total_second(str(now_time))
            # 10秒以上の差があればタイムアウト判定
            if (now_time_second - update_time_second) > 10:
                timeout_count = 1
            else:
                timeout_count = 0

    return timeout_count

# 日時を秒に変換する関数
def total_second(time):
    hour = int(time[-5]) + 10*int(time[-6])
    minutes = int(time[-3]) + 10*int(time[-4])
    second = int(time[-1]) + 10*int(time[-2])
    total_second = hour*360 + minutes*60 + second

    return total_second