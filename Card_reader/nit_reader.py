import nfc
import struct

def read_card(tag):
    service_code = 0x400B

    #16ビットのservice_codeからservice >> 6で上位10ビットを取り出し、service_code && 0x3fで下位6ビットを取り出す
    svcd = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
    #serviceはread_without_encryptionの引数service_list内でのインデックス
    bc_id = nfc.tag.tt3.BlockCode(0,service=0)
    #read_without_encryptionでタグの指定した部分の情報内のブロックデータを読み取る
    block_data = tag.read_without_encryption([svcd], [bc_id])
    #今回ではブロックデータの1文字目から8文字目に格納されている、それを文字列に変換しutf-8でデコード
    student_id = str(block_data[0:8].decode("utf-8"))

    return student_id