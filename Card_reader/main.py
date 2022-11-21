import nfc
import nit_reader
import FeliCa_reader
import manage_db
import play
import pymysql.cursors
import card_type
import timeout

def connected(tag):
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            student_id = FeliCa_reader.read_FeliCa(tag)
            print(student_id)
            c_type = card_type.change_type(student_id)
            timeout_count = timeout.check_timeout(c_type)
            manage_db.search_data(student_id,timeout_count)
            play.playsound()
        except Exception as e:
            try:
                student_id = nit_reader.read_card(tag)
                c_type = card_type.change_type(student_id)
                timeout_count = timeout.check_timeout(c_type)
                manage_db.search_data(student_id,timeout_count)
                play.playsound()
            except Exception as e:
                print("Error:%s" % e)
                play.playerrorsound()
    else:
        print("Error:tag isn't Type3Tag")
        play.playerrorsound()

    #値をTrueで返すと触れて離すまでの間、一回だけ処理を行う
    return True

clf = nfc.ContactlessFrontend('usb')

def main():
    while True:
        #学生証を読み取るまで待機
        clf.connect(rdwr={'on-connect': connected,})


try:
    main()
except KeyboardInterrupt:
    print("Forced termination")
    clf.close()
    sys.exit(0)