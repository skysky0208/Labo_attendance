# Labo_attendance

## Git branch
- master
- developer (バグ修正後マージ)
<br />

## Django
### 導入手順
1. Djangoインストール，プロジェクトの作成
```
$ pip install django
$ django-admin.py startproject プロジェクト名(今回はmysite)
```
2. DBの作成
3. パッケージPyMySQLのインストール
```
$ pip install pymysql
$ pip freeze -l
PyMySQL==0.10.1
```
4. settings.pyのデータベース情報を変更
```python:setting.py
'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Lab_attendance', #DB名
        'USER': 'root',　#USER名
        'PASSWORD': 'admin'　#pass
}
```
5. DBの情報を取得する
```
$ python3 manage.py inspectdb
```
6. model.pyにDB情報を記述
7. DB情報を反映させる
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
### 実行方法
```
$ python3 manage.py runserver
```
実行後 http://127.0.0.1:8000/attendance/attendance_list にアクセス  
<br />

## MySQL
### 導入手順
以下のサイトを参考
https://www.raspberrypirulo.net/entry/mariadb-install

1. MySQLデータベース(Mariadb)のインストール
```
$ sudo apt-get install mariadb-server
　# 途中でrootのパスを入力
```

2. unix_sokectプラグインの無効化
```
$ sudo mysql -u root
MariaDB [(none)]> USE mysql;
MariaDB [mysql]> UPDATE user SET plugin='' WHERE User='root';
MariaDB [mysql]> exit
$ sudo systemctl restart mysql
```

3. rootのパスワード設定
```
$ mysql -u root
MariaDB [(none)]> update mysql.user set password=password('設定したいパスワード') where user = 'root';
MariaDB [mysql]> exit
$ sudo systemctl restart mysql
```

### データベースの作成
1. データベースの追加
```
MariaDB [(none)]> CREATE DATABASE データベース名(今回はLab_attendance);
```

2. 作成したデータベースを確認
```
MariaDB [(none)]> SHOW DATABASES;
```

3. 使用するデータベースの選択
```
MariaDB [(none)]> USE Lab_attendance; #データベース名
```

4. 選択したデータベースにテーブルを作成
```
MariaDB [Lab_attendance]> CREATE TABLE Lab_attendance_tb (user_id INT NOT NULL PRIMARY KEY, user_name VARCHAR(100), status VARCHAR(100), update_time DATETIME, room_id VARCHAR(100), comment TEXT, calendar_id VARCHAR(100));
```
作成したテーブルの詳細は以下を参照

### データベース（Lab_attendance_tb）
データベースのテーブルはuser_id, user_name, status, update_time, room_id, comment, calendar_id で構成
- user_id (Integer) : 学籍番号 (プライマリキー)
- user_name (Char[100]) : 名前
- status (Char[100]) : 入室、退室、外出の状態
- update_time (DateTime): 最終更新日時
- room_id (Char[100]) : 入室している部屋番号
- comment (Text): 自由に設定できるコメント
- calendar_id (Char[100]) : カレンダー連携のためのID
<br />

## Speaker・CardReader
### 初期設定
1. simpleaudioライブラリ，nfcpyライブラリのインストール
```
$ sudo apt-get install -y python3-pip libasound2-dev
$ pip3 install simpleaudio
$ sudo pip3 install -U nfcpy
$ pip3 list | grep nfcpysi
```

2. ラズパイの音声出力をイヤホンジャックに変更
```
$ sudo nano /boot/config.txt
------------------------------------
# 変更前 (33行目あたり)
# hdmi_drive=2

# 変更後
hdmi_drive=1
```

3. wavファイルをmacからラズパイにコピー
mac側で転送元のファイルがあるディレクトリに移動
```
$ scp error.wav pi@ラズパイのIPアドレス:/home/pi/Music
$ scp success.wav pi@ラズパイのIPアドレス:/home/pi/Music
```
<br />

## RaspberryPi関連

### 自動実行設定
以下のサイトを参考  
https://qiita.com/molchiro/items/ee32a11b81fa1dc2fd8d

1. 自動起動するプログラムを置く、ディレクトの作成
```
$ sudo mkdir /opt/Lab_attendance
```

2. 自動起動するプログラムの作成  
```
$ cd /opt/Lab_attendance
``` 

```
# /home/pi/Lab_attendance/Labo_attendance/Card_reader/のプログラムをコピペ
$ sudo nano 作成するプログラム(6個)
```

3. serviceファイルを作成  
```
$ sudo nano /etc/systemd/system/Lab_attendance.service
```

```Lab_attendance.service
[Unit]
Description=start Lab_attendance system
After=network.target mysqld.service

[Service]
ExecStart=/usr/bin/python3 main.py
WorkingDirectory=/opt/Lab_attendance
User=root

[Install]
WantedBy=multi-user.target
```
4. serviceファイルをenable
```
$ sudo systemctl enable Lab_attendance.service
```
5. rebootして確認
<br />

### タイムスケジューラcron
1. cronの動作確認
```
sudo /etc/init.d/cron status
```
2. cronの設定
```
sudo cp /etc/crontab /etc/cron.d/cron_test
sudo vi /etc/cron.d/cron_test 
========================================
# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
(例)
0 0 * * 0 root python3 /home/pi/Lab_attendance/Labo_attendance/mysite/manage.py report_mail
0 0 * * * root python3 /home/pi/Lab_attendance/Labo_attendance/mysite/manage.py data_reset
```
3. cronの再起動
```
sudo service cron restart
```
<br />

## Requirement
* Django 3.0.6
* mySQL Ver 15.1 Distrib 10.3.31-MariaDB
* Python 3.7.3
* PyMySQL 0.10.1
* google-api-python-client 1.12.10
* google-auth-httplib2     0.1.0
* google-auth-oauthlib     0.4.1
* nfcpy     1.0.3 
* simpleaudio   1.0.4 


# commit rule

```
🎉  :tada: 初めてのコミット
🔖  :bookmark: バージョンタグ
✨  :sparkles: 新機能
🐛  :bug: バグ修正
✏️  :pencil2: タイポ修正
💩  :poop: 要修正コード
🚽  :toilet: 要修正コード修正
📚  :books: ドキュメント
💬  :speech_balloon: ソースコメント
🎨  :art: デザインUI/UX
🚨  :rotating_light: テスト
✅  :white_check_mark: テスト通過
🚧  :construction: 未完成
🔥  :fire: ファイル消去
🚚  :truck: ファイル移動
🔧  :wrench: conf file
🔀  :twisted_rightwards_arrows: マージ
```