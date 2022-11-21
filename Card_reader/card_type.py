import pymysql.cursors
import nit_reader

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
                    
# 一時退出用のカードか学生用のカードか判定
def change_type(student_id):
    with connection.cursor() as cursor:
        # カードの種類を判定する変数
        #　初期値は'STU_CARD'としておく
        c_type = 'STU_CARD'

        # student_idを探索
        sql = "SELECT user_id FROM Lab_attendance_tb WHERE user_id = %s"
        # student_idをmatch_idとする
        cursor.execute(sql, (student_id))
        match_id = cursor.fetchone()['user_id']

        # user_nameをmatch_nameとする
        sql = "SELECT user_name FROM Lab_attendance_tb WHERE user_id = %s"
        cursor.execute(sql, (student_id))
        match_name = cursor.fetchone()['user_name']

        # DBにstudent_idが登録されていない場合
        if match_id is None:
            print("Error:Unregistered data")

        # DBにstudent_idが登録されている場合
        else:
            if match_name == 'EXIT CARD':
                # statusをmatch_statusとする
                sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = %s"
                cursor.execute(sql, ('1', student_id))
                connection.commit()
                print("#USING EXIT CARD")
                c_type = 'EXIT_CARD'
            else:
                print("#USING STU CARD")
                c_type = 'STU_CARD'
        
        cursor.close()
        return c_type
