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
                    

def search_data(student_id,timeout_count):
    with connection.cursor() as cursor:
        # student_idを探索
        sql = "SELECT user_id FROM Lab_attendance_tb WHERE user_id = %s"
        # student_idをmatch_idとして取得
        cursor.execute(sql, student_id)
        match_id = cursor.fetchone()['user_id']

        # statusをmatch_statusとして取得
        sql = "SELECT status FROM Lab_attendance_tb WHERE user_id = %s"
        cursor.execute(sql, student_id)
        match_status = cursor.fetchone()['status']

        # user_nameをmatch_nameとして取得
        sql = "SELECT user_name FROM Lab_attendance_tb WHERE user_id = %s"
        cursor.execute(sql, student_id)
        match_name = cursor.fetchone()['user_name']

        # DBにstudent_idが登録されていない場合
        if match_id is None:
            print("Error:Unregistered data")
        # DBにstudent_idが登録されている場合
        else: 
            # EXIT_CARDのタイムアウト処理
            if timeout_count == 1:
                sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_name = 'EXIT CARD'"
                cursor.execute(sql, '0')
                connection.commit()
                print("TIMEOUT EXIT CARD")
            elif timeout_count == 0:
                print("AVAILABLE EXIT CARD")
            
            # EXIT_CARDのstatusを取得
            sql = "SELECT status FROM Lab_attendance_tb WHERE user_name LIKE 'EXIT CARD'"
            cursor.execute(sql)
            match_type = cursor.fetchone()['status']
            if match_name == 'EXIT CARD':
                print(match_name + "\n")
            else:
                print(match_name)

            # EXIT_CARDのstatusが0の場合(EXIT_CARD未使用)
            if match_name != 'EXIT CARD' and match_type == '0':
                print("---UPDATE DATA---")
                # 退出から入室に更新
                if match_status == 'absent':
                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = %s"
                    cursor.execute(sql, ('attend', student_id))
                    connection.commit()
                    sql = "UPDATE Lab_attendance_tb SET room_id = %s WHERE user_id = %s"
                    cursor.execute(sql, ('16_321', student_id))
                    connection.commit()
                    print("退出->入室\n")
                # 入室から退出に更新
                elif match_status == 'attend':
                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = %s"
                    cursor.execute(sql, ('absent', student_id))
                    connection.commit()
                    sql = "UPDATE Lab_attendance_tb SET room_id = NULL WHERE user_id = %s"
                    cursor.execute(sql, student_id)
                    connection.commit()
                    print("入室->退出\n")
                # 一時退出から入室に更新
                else:
                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = %s"
                    cursor.execute(sql, ('attend', student_id))
                    connection.commit()
                    sql = "UPDATE Lab_attendance_tb SET room_id = %s WHERE user_id = %s"
                    cursor.execute(sql, ('16_321', student_id))
                    connection.commit()
                    print("一時退室->入室\n")

            # EXIT_CARDのstatusが1の場合(EXIT_CARD使用)
            elif match_name != 'EXIT CARD' and match_type == '1':
                print("---UPDATE DATA---")
                # 退出から入室に更新
                if match_status == 'absent':
                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = %s"
                    cursor.execute(sql, ('attend', student_id))
                    connection.commit()
                    sql = "UPDATE Lab_attendance_tb SET room_id = %s WHERE user_id = %s"
                    cursor.execute(sql, ('16_321', student_id))
                    connection.commit()
                    print("退出->入室")

                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_name = 'EXIT CARD'"
                    cursor.execute(sql, '0')
                    connection.commit()
                    print("USED EXIT CARD\n")

                # 入室から一時退出に更新
                elif match_status == 'attend':
                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = %s"
                    cursor.execute(sql, ('lab out', student_id))
                    connection.commit()
                    sql = "UPDATE Lab_attendance_tb SET room_id = NULL WHERE user_id = %s"
                    cursor.execute(sql, student_id)
                    connection.commit()
                    print("入室->一時退出")

                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_name = 'EXIT CARD'"
                    cursor.execute(sql, '0')
                    connection.commit()
                    print("USED EXIT CARD\n")

                # 一時退出から入室に更新
                else:
                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = %s"
                    cursor.execute(sql, ('attend', student_id))
                    connection.commit()
                    sql = "UPDATE Lab_attendance_tb SET room_id = %s WHERE user_id = %s"
                    cursor.execute(sql, ('16_321', student_id))
                    connection.commit()
                    print("一時退室->入室")

                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_name = 'EXIT CARD'"
                    cursor.execute(sql, '0')
                    connection.commit()
                    print("USED EXIT CARD\n")

            else:
                print(end='')
        
        cursor.close()
        return match_id