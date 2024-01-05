import struct
import json
import zlib
from datetime import datetime

class LogMessage:
    def __init__(self, header, message, level, file, line):
        self.timestamp = datetime.now()
        self.header = header #remove header fields
        self.message = message
        self.level = level
        self.file = file
        self.line = line

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "header": self.header,
            "message": self.message,
            "level": self.level,
            "file": self.file,
            "line": self.line
        }

    def to_json(self):
        return json.dumps(self.to_dict()).encode("utf-8")
    
    @classmethod
    def from_bytes(cls, byte_data):
        log_dict = json.loads(byte_data.decode("utf-8"))
        timestamp = datetime.fromisoformat(log_dict["timestamp"])
        return cls(log_dict["header"], log_dict["message"], log_dict["level"], log_dict["file"], log_dict["line"])

    def add_header(serialized_data):
        # Calculate CRC32 for serialized data
        crc_value = zlib.crc32(serialized_data)

        length_bytes = len(serialized_data).to_bytes(2, 'little')
        crc_bytes = crc_value.to_bytes(4, 'little')
        header_bytes = bytes([0xd7]) + length_bytes + crc_bytes
        # Create a new structure with type + length + CRC + serialized data
        # length_bytes = json.dumps(len(serialized_data)).encode("utf-8")
        # crc_bytes = json.dumps(crc_value).encode("utf-8")

        return header_bytes + serialized_data

    @classmethod
    def from_bytes_with_header(cls, byte_data_with_header):
        # Extract length and CRC THIS IS WHERE THE ERROR IS
        length = int.from_bytes(byte_data_with_header[1:3], 'little')
        crc = int.from_bytes(byte_data_with_header[3:7], 'little')

        # Extract serialized data
        serialized_data = byte_data_with_header[7:]

        # Verify CRC
        calculated_crc = zlib.crc32(serialized_data)
        if calculated_crc != crc:
            raise ValueError("CRC check failed. Data may be corrupted.")

        # Deserialize the object
        log_message = cls.from_bytes(serialized_data)

        return log_message

    def to_bytes_packet(self):
        # Assuming the packet structure is: [timestamp][length of header][header][length of message][message][level][file][line]
        timestamp_bytes = struct.pack("!Q", int(self.timestamp.timestamp()))
        header_with_crc = self.to_bytes_with_header()

        return timestamp_bytes + header_with_crc

    def set_header(self, new_header):
        self.header = new_header

    def display(self):
        if self.header:
            print(f"{self.timestamp} - {self.header}: {self.level} - {self.message} (File: {self.file}, Line: {self.line})")
        else:
            print(f"{self.timestamp} - {self.level} - {self.message} (File: {self.file}, Line: {self.line})")

    def __str__(self):
        return f"{self.timestamp} - {self.header} - {self.level} - {self.message} (File: {self.file}, Line: {self.line})"
