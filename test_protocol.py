from log_message import LogMessage
import protocol

def test_protocol_multi():
    msg = LogMessage(None, "hello", "debug", "filename.py", 1)
    pickle_msg = protocol.encode_pickle(msg)
    json_msg = protocol.encode_json(msg)
    cbor_msg = protocol.encode_cbor(msg)

    decoded = protocol.decode_message(pickle_msg)
    assert decoded.message == msg.message
    decoded = protocol.decode_message(json_msg)
    assert decoded.message == msg.message
    decoded = protocol.decode_message(cbor_msg)
    assert decoded.message == msg.message


def test_protocol_wrong_type_id():
    bad_message = [0xd1, 0, 0, 0, 0, 0, 0, 0]
    protocol.decode_message(bad_message)

def test_protocol_bad_length():
    bad_message = protocol.encode_with_header(protocol.ENCODING_JSON, [1])
    bad_message[1] = 0xff
    protocol.decode_message(bad_message)

def test_protocol_bad_crc():
    bad_message = protocol.encode_with_header(protocol.ENCODING_JSON, [1])
    bad_message[3] = bad_message[3] ^ 0x70
    protocol.decode_message(bad_message)