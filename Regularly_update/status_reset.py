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

# statusを退室にリセット
def status_reset():
    with connection.cursor() as cursor:
        # DB内のすべての要素を抽出
        sql = "SELECT * FROM Lab_attendance_tb"
        cursor.execute(sql)
        all_dates = cursor.fetchall()

        # 全ての要素に対して条件比較
        for date in all_dates:
            # EXITカードでなければ退室に更新
            if date['user_name'] != "EXIT CARD" :
                sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = " + str(date['user_id']) 
                cursor.execute(sql, 'absent')
                connection.commit()
        print("Have Reseted DateBase")
