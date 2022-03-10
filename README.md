# Labo_attendance


## Git branch
- master
- developer (バグ修正後マージ)

# Requirement
* Django 3.0.6
* mySQL Ver 15.1 Distrib 10.3.31-MariaDB
* Python 3.7.3

## Django
### ページ構成
- attendance/attendance_list　出席情報閲覧ページ(トップページ)
- attendance/user_create　ユーザ登録ページ
- attendance/comment_update　コメント編集ページ
### CSS
- Boostrapを用いて体裁を整える
- それぞれのhtmlファイルに対応したcssファイル

## MySQL
データベースのテーブルはuser_id, user_name, status, update_time, room_id, comment で構成
- user_id (Integer) : 学籍番号 (プライマリキー)
- user_name (Char[100]) : 名前
- status (Char[100]) : 入室、退室、外出の状態
- update_time (DateTime): 最終更新日時
- room_id (Char[100]) : 入室している部屋番号
- comment (Char[100]): 自由に設定できるコメント

## CardReader

## commit rule

```
🎉  :tada: 初めてのコミット
🔖  :bookmark: バージョンタグ
✨  :sparkles: 新機能
🐛  :bug: バグ修正
✏️  :pencil2: タイポ修正
💩  :poop: うんコード/要修正
🚽  :toilet: うんコード修正
♻️  :recycle: リファクタリング
⏪  :rewind: リベース
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
