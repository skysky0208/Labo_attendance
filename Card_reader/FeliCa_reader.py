import nfc
import binascii

def read_FeliCa(tag):
    student_id = binascii.hexlify(tag.idm)

    return student_id