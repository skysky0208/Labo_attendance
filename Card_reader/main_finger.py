import ConvertID
import manage_db
import play
import pymysql.cursors
import Finger_reader
import time
import nfc
import FeliCa_reader
import card_type
import timeout

def fingerprint():
    try:
        positionNumber = Finger_reader.FingerNum()
        print(positionNumber)
        student_id = ConvertID.convert_data(positionNumber)
        print(student_id)
        '''
        timeout_count = timeout.check_timeout(c_type)
        timeout_count = 1
        manage_db.search_data(student_id,timeout_count)
       play.playsound()
       '''
    except Exception as e:
        print("Error:%s" % e)
        play.playerrorsound()
        fingerprint()
        time.sleep(1)
   
    #値をTrueで返すと触れて離すまでの間、一回だけ処理を行う
    return True

def main():
    while True:
        fingerprint()
        time.sleep(1)

try:
    main()
except KeyboardInterrupt:
    print("Forced termination")
    sys.exit(0)

if __name__ == "__main__":
    main()