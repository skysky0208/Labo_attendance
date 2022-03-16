import datetime
import time
import schedule
from status_reset import status_reset
from update_comment import update_comment

def date_change():
    # 日付変更時に関数job()を実行
    schedule.every().day.at("16:56").do(date_change_process)

    while True:
        # 1分毎に条件比較
        schedule.run_pending()
        time.sleep(60)

# 日付変更時処理
def date_change_process():
    status_reset()
    update_comment()