import struct
import pickle
import zlib
from datetime import datetime

class LogMessage:
    def __init__(self, header, message, level, file, line):
        self.timestamp = datetime.now()
        self.header = header
        self.message = message
        self.level = level
        self.file = file
        self.line = line

    def to_bytes(self):
        return pickle.dumps(self)

    @classmethod
    def from_bytes(cls, byte_data):
        return pickle.loads(byte_data)

    def add_header(self, new_header_type):
        # Add or update the header type
        self.header_type = new_header_type

    def to_bytes_with_header(self):
        # Serialize the object
        serialized_data = self.to_bytes()

        # Calculate CRC32 for serialized data
        crc_value = zlib.crc32(serialized_data)

        # Create a new structure with type + length + CRC + serialized data
        header_type_bytes = struct.pack("!H", self.header_type)
        length_bytes = struct.pack("!H", len(serialized_data))
        crc_bytes = struct.pack("!I", crc_value)

        return header_type_bytes + length_bytes + crc_bytes + serialized_data

    @classmethod
    def from_bytes_with_header(cls, byte_data_with_header):
        # Extract header type, length, and CRC
        header_type = struct.unpack("!H", byte_data_with_header[:2])[0]
        length = struct.unpack("!H", byte_data_with_header[2:4])[0]
        crc = struct.unpack("!I", byte_data_with_header[4:8])[0]

        # Extract serialized data
        serialized_data = byte_data_with_header[8:]

        # Verify CRC
        calculated_crc = zlib.crc32(serialized_data)
        if calculated_crc != crc:
            raise ValueError("CRC check failed. Data may be corrupted.")

        # Deserialize the object
        log_message = cls.from_bytes(serialized_data)

        # Update the header type
        log_message.add_header(header_type)

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
