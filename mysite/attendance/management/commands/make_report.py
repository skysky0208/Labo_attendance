import numpy as np

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date, timedelta, datetime, time
from .get_data import get_data, get_h_m


# フォントを登録
registerFont(TTFont('GenShinGothic',
                    './static/font_data/GenShinGothic-Monospace-Medium.ttf'))


def avarage_enter_time(query):
    total_enter_timestamp = 0
    total_date = 0

    for i in range(len(query)) :
        
        timestamp = timedelta(
            hours=query[i].hour,
            minutes=query[i].minute,
            seconds=query[i].second
        ).total_seconds()
        if(timestamp != 0):
            timestamp = int(timestamp/60)
            total_enter_timestamp = total_enter_timestamp + timestamp
            total_date = total_date + 1
        
    if (total_enter_timestamp != 0):
        avarage_enter_timestamp = total_enter_timestamp / total_date
    else :
        avarage_enter_timestamp = 0

    return avarage_enter_timestamp


def make_report(user_id, date, enter_time, stay_time, lastweek_enter_time, lastweek_stay_time):
    file_path = './static/report/' + str(user_id) + '.pdf'  # 出力ファイル名を設定
    graph_path = "./static/graph/" + str(user_id) + ".jpg"

    paper = canvas.Canvas(file_path)  # 白紙のキャンバスを用意
    paper.saveState()  # 初期化
    paper.setFont('GenShinGothic', 20)  # フォントを設定

    # 横wと縦hの用紙サイズを設定
    w = 210 * mm
    h = 220 * mm

    paper.setPageSize((w, h))  # 用紙のサイズをセット
    title1 = "大塚研究室　出席週間レポート" 
    title2 = str(date[0]) + "～" + str(date[4])
    paper.drawString(w/2 - 130, h - 60, title1) # テキストの書き込み

    paper.setFont('GenShinGothic', 18)  # フォントを設定
    paper.drawString(w/2 - 100, h - 85, title2) # テキストの書き込み

    # 画像を埋め込み(画像ファイルのパス, 横位置, 縦位置, 画像横サイズ, 画像縦サイズ)
    paper.drawInlineImage(graph_path, 31*mm, h-150*mm, 148*mm, 111*mm)
    paper.setFont('GenShinGothic', 15)  # フォントを設定

    paper.setFont('GenShinGothic', 13)  # フォントを設定

    # 今週の平均入室時間と合計滞在時間
    thisweek_enter_time_hour, thisweek_enter_time_minute = get_h_m(avarage_enter_time(enter_time))
    thisweek_stay_time_hour, thisweek_stay_time_minute = get_h_m(sum(stay_time))

    # 先週の平均入室時間と合計滞在時間
    lastweek_enter_time_hour, lastweek_enter_time_minute = get_h_m(avarage_enter_time(lastweek_enter_time))
    lastweek_stay_time_hour, lastweek_stay_time_minute = get_h_m(sum(lastweek_stay_time))

    enter_time_info = "平均入室時間：　"
    enter_time_info = enter_time_info + "先週…" + str(lastweek_enter_time_hour) + "時" + str(lastweek_enter_time_minute) + "分　"
    enter_time_info = enter_time_info + "今週…" + str(thisweek_enter_time_hour) + "時" + str(thisweek_enter_time_minute) + "分"

    stay_time_info = "合計在室時間：　"
    stay_time_info = stay_time_info + "先週…" + str(lastweek_stay_time_hour) + "時間" + str(lastweek_stay_time_minute) + "分　"
    stay_time_info = stay_time_info + "今週…" + str(thisweek_stay_time_hour) + "時間" + str(thisweek_stay_time_minute) + "分　"

    paper.drawString(w/2-150, 61*mm, enter_time_info)

    enter_time_ratio_hour, enter_time_ratio_minute = get_h_m(avarage_enter_time(enter_time) - avarage_enter_time(lastweek_enter_time))
    paper.drawString(w/2-10, 52*mm, '平均入室時間先週比 ' + str(enter_time_ratio_hour) + '時間' + str(enter_time_ratio_minute) + '分')

    paper.drawString(w/2-150, 32*mm, stay_time_info)

    if(sum(lastweek_stay_time) != 0):
        stay_time_ratio = int(sum(stay_time)/sum(lastweek_stay_time)*100)
        paper.drawString(w/2+10, 24*mm, '滞在時間先週比 ' + str(stay_time_ratio) + '％')    

    paper.save()  # PDFを保存

    context_info = []
    context_info.append(str(thisweek_enter_time_hour) + "時" + str(thisweek_enter_time_minute) + "分")
    context_info.append(str(lastweek_enter_time_hour) + "時" + str(lastweek_enter_time_minute) + "分")
    context_info.append(str(enter_time_ratio_hour) + '時間' + str(enter_time_ratio_minute) + '分')
    context_info.append(str(thisweek_stay_time_hour) + "時間" + str(thisweek_stay_time_minute) + "分")
    context_info.append(str(lastweek_stay_time_hour) + "時間" + str(lastweek_stay_time_minute) + "分")
    if(sum(lastweek_stay_time) != 0):
        stay_time_ratio = int(sum(stay_time)/sum(lastweek_stay_time)*100)
        context_info.append(str(stay_time_ratio) + '％')

    return context_info

    