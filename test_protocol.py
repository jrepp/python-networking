from log_message import LogMessage
import protocol

def test_protocol_multi():
    msg = LogMessage(None, "hello", "debug", "filename.py", 1)
    pickle_msg = protocol.encode_pickle(msg)
    json_msg = protocol.encode_json(msg)
    cbor_msg = protocol.encode_cbor(msg)

    protocol.decode_message(pickle_msg)
    protocol.decode_message(json_msg)
    protocol.decode_message(cbor_msg)