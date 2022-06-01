import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages 

def make_graph(user_id, date, enter_time, stay_time):
    # 横軸(日付)
    x = date

    # 縦軸(入室時刻)
    y1 = enter_time
    today = datetime.date.today()
    y1 = [datetime.datetime.combine(today, slot) for slot in y1]

    # 縦軸(在席時間)
    y2 = stay_time

    df = pd.DataFrame(
        {
        'x': x,
        'y1': y1,
        'y2': y2
        }
    )

    #第一軸(ax1)と第二軸(ax2)を作って関連付ける
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    #第一軸折れ線グラフ
    ax1.plot(df['x'], df['y1'], linestyle="solid",color="crimson",marker="o")

    # 第二軸棒グラフ
    ax2.bar(df['x'], df['y2'],color="lightblue",align="center")

    #重ね順として折れ線グラフを前面に。
    ax1.set_zorder(2)
    ax2.set_zorder(1)

    #折れ線グラフの背景を透明に。
    ax1.patch.set_alpha(0)

    # 横軸メモリ間隔を1日に設定
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    # 縦軸メモリ間隔を1時間に設定
    ax1.yaxis.set_major_locator(mdates.HourLocator())

    #フォーマットを変更
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.set_major_formatter(mdates.DateFormatter('%H:%M:'))

    plt.show()

    # save figure
    fig.savefig( "./static/graph/" + str(user_id) + ".jpg")

