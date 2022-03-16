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

## CardReader
<br />

## GoogleCalendar連携
### 導入手順
1. Google client library インストール
```
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
2. 認証し，credentianls.jsonを同ディレクトリに配置する
<br />

## Requirement
* Django 3.0.6
* mySQL Ver 15.1 Distrib 10.3.31-MariaDB
* Python 3.7.3
* PyMySQL 0.10.1
* google-api-python-client 1.12.10
* google-auth-httplib2     0.1.0
* google-auth-oauthlib     0.4.1

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