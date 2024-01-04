import pickle
import zlib



def create_message(log_object):
    object_bytes = pickle.dumps(log_object)
    length_bytes = len(object_bytes).to_bytes(2, 'little')
    crc_bytes = zlib.crc32(object_bytes).to_bytes(4, 'little')
    header_bytes = bytes([0xd7]) + length_bytes + crc_bytes
    
    message_bytes = header_bytes + object_bytes
    return message_bytes

def decode_message(message_bytes):
    if message_bytes[0] != 0xd7:
        raise Exception("Invalid message type")

    provided_len = int.from_bytes(message_bytes[1:2], 'little')
    if provided_len < len(message_bytes) - 7:
        raise Exception("Invalid message length")
    
    object_bytes = message_bytes[7:]
    provided_crc = int.from_bytes(message_bytes[3:6], 'little')
    calculated_crc = zlib.crc32(object_bytes)
    if provided_crc != calculated_crc:
        raise Exception(f"Invalid crc {provided_crc} != {calculated_crc} ({object_bytes})")
    
    obj = pickle.loads(object_bytes)
    return obj