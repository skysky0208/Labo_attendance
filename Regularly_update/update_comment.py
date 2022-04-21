import pymysql.cursors
from get_event import get_event_from_calendarIDs

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
def update_comment():
    with connection.cursor() as cursor:
        # DB内のすべての要素を抽出
        sql = "SELECT * FROM Lab_attendance_tb"
        cursor.execute(sql)
        all_data = cursor.fetchall()

        all_today_events = get_event_from_calendarIDs([d.get('calendar_id') for d in all_data])

        # 全ての要素に対して条件比較
        for i in range(len(all_data)):
            # EXITカードでなければ退室に更新
            sql = "UPDATE Lab_attendance_tb SET comment = %s WHERE user_id = " + str(all_data[i]['user_id']) 
            cursor.execute(sql, all_today_events[i])
            connection.commit()
        print("Have updated comments")