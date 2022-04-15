import ConvertID
import manage_db
import play
import pymysql.cursors
import Finger_reader
import time
import sys
import sw

def fingerprint():
    try:
        positionNumber = Finger_reader.FingerNum()
        print(positionNumber)
        student_id = ConvertID.convert_data(positionNumber)
        print(student_id)
        exit_count = sw.switch_state()
        print(exit_count)
        manage_db.search_data(student_id,exit_count)
        play.playsound()
        
    except Exception as e:
        print("Error:%s" % e)
        play.playerrorsound()
        fingerprint()
        time.sleep(0.7)
   
    #値をTrueで返すと触れて離すまでの間、一回だけ処理を行う
    return True

def main():
    while True:
        fingerprint()
        time.sleep(0.7)

try:
    main()
except KeyboardInterrupt:
    print("Forced termination")
    sys.exit(0)