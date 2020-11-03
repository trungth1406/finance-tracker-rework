import binascii
import sqlite3
import zlib
from distutils.log import log
from datetime import datetime


def get_new_contents(file_location="/Users/trungtran/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite",
                     folder_name="CHI TIÊU",
                     possible_file_name=f"Tháng {datetime.now().strftime('%m')}"):
    conn = sqlite3.connect(file_location)
    cursor = conn.cursor()
    query = " SELECT n.Z_PK, n.ZNOTE as note_id, n.ZDATA as data, " \
            " c3.ZFILESIZE, " \
            " c4.ZFILENAME, c4.ZIDENTIFIER as att_uuid,  " \
            " c1.ZTITLE1 as title, c1.ZSNIPPET as snippet, c1.ZIDENTIFIER as noteID, " \
            " c1.ZCREATIONDATE1 as created, c1.ZLASTVIEWEDMODIFICATIONDATE, c1.ZMODIFICATIONDATE1 as modified, " \
            " c2.ZACCOUNT3, c2.ZTITLE2 as folderName, c2.ZIDENTIFIER as folderID, " \
            " c5.ZNAME as acc_name, c5.ZIDENTIFIER as acc_identifier, c5.ZACCOUNTTYPE, " \
            " c3.ZSUMMARY, c3.ZTITLE, c3.ZURLSTRING, c3.ZTYPEUTI " \
            " FROM ZICNOTEDATA as n " \
            " LEFT JOIN ZICCLOUDSYNCINGOBJECT as c1 ON c1.ZNOTEDATA = n.Z_PK  " \
            " LEFT JOIN ZICCLOUDSYNCINGOBJECT as c2 ON c2.Z_PK = c1.ZFOLDER " \
            " LEFT JOIN ZICCLOUDSYNCINGOBJECT as c3 ON c3.ZNOTE= n.ZNOTE " \
            " LEFT JOIN ZICCLOUDSYNCINGOBJECT as c4 ON c4.ZATTACHMENT1= c3.Z_PK " \
            " LEFT JOIN ZICCLOUDSYNCINGOBJECT as c5 ON c5.Z_PK = c1.ZACCOUNT2  " \
            " ORDER BY note_id  "
    cursor.row_factory = sqlite3.Row
    cursor.execute(query)
    lines = []
    for row in cursor:
        try:
            if folder_name in row['folderName']:
                if possible_file_name in row['title']:
                    data = get_uncompressed_data(row['data'])
                    text_content = process_body_blob(data)
                    lines = text_content.split("\n")
        except sqlite3.Error:
            print("Error")
    conn.close()
    return lines


def get_uncompressed_data(compressed):
    if compressed is None:
        return None
    data = None
    try:
        data = zlib.decompress(compressed, 15 + 32)
    except zlib.error:
        log.exception('Zlib Decompression failed!')
    return data


def process_body_blob(blob):
    data = b''
    if blob is None:
        return data
    try:
        pos = 0
        if blob[0:3] != b'\x08\x00\x12':  # header
            log.error('Unexpected bytes in header pos 0 - ' + binascii.hexlify(blob[0:3]) + '  Expected 080012')
            return ''
        pos += 3
        length, skip = read_field_length(blob[pos:])
        pos += skip

        if blob[pos:pos + 3] != b'\x08\x00\x10':  # header 2
            log.error('Unexpected bytes in header pos {0}:{0}+3'.format(pos))
            return ''
        pos += 3
        length, skip = read_field_length(blob[pos:])
        pos += skip

        # Now text data begins
        if blob[pos] != 0x1A:
            log.error('Unexpected byte in text header pos {} - byte is 0x{:X}'.format(pos, blob[pos]))
            return ''
        pos += 1
        length, skip = read_field_length(blob[pos:])
        pos += skip
        # Read text tag next
        if blob[pos] != 0x12:
            log.error('Unexpected byte in pos {} - byte is 0x{:X}'.format(pos, blob[pos]))
            return ''
        pos += 1
        length, skip = read_field_length(blob[pos:])
        pos += skip
        data = blob[pos: pos + length].decode('utf-8', 'backslashreplace')
        # Skipping the formatting Tags
    except (IndexError, ValueError):
        log.exception('Error processing note data blob')
    return data


def read_field_length(blob):
    """Returns a tuple (length, skip) where skip is number of bytes read"""
    length = 0
    skip = 0
    try:
        data_length = int(blob[0])
        length = data_length & 0x7F
        while data_length > 0x7F:
            skip += 1
            data_length = int(blob[skip])
            length = ((data_length & 0x7F) << (skip * 7)) + length
    except (IndexError, ValueError):
        log.exception('Error trying to read length field in note data blob')
    skip += 1
    return length, skip
