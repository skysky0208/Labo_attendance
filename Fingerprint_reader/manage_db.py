#!/usr/bin/python3
import sys
sys.path.insert(0,"/home/pi/.local/lib/python3.7/site-packages")
import pymysql.cursors
import play
import Data_collection


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

def search_data(student_id,exit_count):
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
        
        # update_timeをtmp_timeとして取得
        sql = "SELECT DATE_FORMAT(update_time, %s) AS update_time FROM Lab_attendance_tb WHERE user_id = %s"
        cursor.execute(sql, ('%H%i%s', student_id))
        tmp_time = cursor.fetchone()['update_time']

        # DBにstudent_idが登録されていない場合
        if match_id is None:
            print("Error:Unregistered data")
            play.playerrorsound()
        # DBにstudent_idが登録されている場合
        else: 
            # 日時更新
            sql = "UPDATE Lab_attendance_tb SET update_time = CAST(NOW() as DATETIME) WHERE user_id = %s"
            cursor.execute(sql, student_id)
            connection.commit()
            
            # EXIT_CARDのstatusが0の場合(EXIT_CARD未使用)
            if exit_count == 0:
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
                    print(tmp_time)

                # 入室から退出に更新
                elif match_status == 'attend':
                    sql = "UPDATE Lab_attendance_tb SET status = %s WHERE user_id = %s"
                    cursor.execute(sql, ('absent', student_id))
                    connection.commit()
                    sql = "UPDATE Lab_attendance_tb SET room_id = NULL WHERE user_id = %s"
                    cursor.execute(sql, student_id)
                    connection.commit()
                    print("入室->退出\n")
                    #滞在記録を登録
                    Data_collection.collect_data(student_id,tmp_time)

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
            elif exit_count == 1:
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
                    #滞在記録を登録
                    Data_collection.collect_data(student_id,tmp_time)

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