import json
import pickle
import zlib
import cbor2
import hexdump

from log_message import LogMessage

# type + len + crc
HEADER_LEN = 1 + 2 + 4

ENCODING_PICKLE = 0xd7
ENCODING_JSON = 0xd8
ENCODING_CBOR = 0xd9


DECODERS = {
    ENCODING_PICKLE: lambda m: pickle.loads(m),
    ENCODING_JSON: lambda m: json.loads(m),
    ENCODING_CBOR: lambda m: cbor2.loads(m),
}

def encode_with_header(type_id, object_bytes):
    length_bytes = len(object_bytes).to_bytes(2, 'little')
    crc_bytes = zlib.crc32(object_bytes).to_bytes(4, 'little')
    header_bytes = bytes([type_id]) + length_bytes + crc_bytes
    return header_bytes + object_bytes

def encode_pickle(log_object) -> bytes:
    return encode_with_header(ENCODING_PICKLE, pickle.dumps(log_object))

def encode_json(log_object) -> bytes:
    return encode_with_header(ENCODING_JSON, log_object.to_json())

def encode_cbor(log_object) -> bytes:
    return encode_with_header(ENCODING_CBOR, cbor2.dumps(log_object.to_dict()))


def decode_message(message_bytes):
    if len(message_bytes) < HEADER_LEN:
        raise Exception(f"message too small for required header {HEADER_LEN}")

    msg_type_id = message_bytes[0]
    msg_len = int.from_bytes(message_bytes[1:2], 'little')
    msg_crc = int.from_bytes(message_bytes[3:7], 'little')
    message_bytes = message_bytes[7:]

    if msg_type_id not in DECODERS.keys():
        raise Exception(f"Unknown message type {msg_type_id}")

    if msg_len < len(message_bytes):
        raise Exception(f"Invalid message length {msg_len} != {len(message_bytes)}")

    calculated_crc = zlib.crc32(message_bytes)
    if msg_crc != calculated_crc:
        raise Exception(f"Invalid CRC {msg_crc} != {calculated_crc} ({hexdump.dump(message_bytes)})")
    

    return DECODERS.get(msg_type_id)(message_bytes)
