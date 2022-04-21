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

# 入退室データの初期値を追加する
def set_date():
    with connection.cursor() as cursor:
        # その日の日付を取得
        sql = "SELECT CURDATE()+0;"
        cursor.execute(sql)
        date = cursor.fetchone()['CURDATE()+0']
        year,month,day = split_date(str(date))
        # DB内のすべてのstudent_idを抽出
        sql = "SELECT user_id FROM Lab_attendance_tb"
        cursor.execute(sql)
        all_student_id = cursor.fetchall()

        # 全てのstudent_idに対して日付を設定
        for student_id in all_student_id:
            sql = "INSERT INTO Lab_attendance_info(student_id, year, month, day, Staytime) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (student_id, year, month, day, 0))
            connection.commit()
        print("Have Seted DateBase")

# 日付 を分割する関数
def split_date(date): 
    year = date[-8] + date[-7] + date[-6] + date[-5]
    month = date[-4] + date[-3]
    day = date[-2] + date[-1]
    return year, month, day
