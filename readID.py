#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import binascii
import nfc

#弊学の学生証の学籍番号が格納されているサービスコード
service_code = 0x400B

def connected(tag):

    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            #16ビットのservice_codeからservice >> 6で上位10ビットを取り出し、service_code && 0x3fで下位6ビットを取り出す
            svcd = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
            #serviceはread_without_encryptionの引数service_list内でのインデックス
            blcd = nfc.tag.tt3.BlockCode(0,service=0)
            #read_without_encryptionでタグの指定した部分の情報内のブロックデータを読み取る
            block_data = tag.read_without_encryption([svcd], [blcd])
            #今回ではブロックデータの1文字目から8文字目に格納されている、それを文字列に変換しutf-8でデコード
            student_id = str(block_data[0:8].decode("utf-8"))
            print(student_id)
        except Exception as e:
            print("Error:%s" % e)
    else:
        print("Error:tag isn't Type3Tag")

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