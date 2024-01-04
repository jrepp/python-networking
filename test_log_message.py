# test_log_message.py
import pytest
import pickle
import zlib
import protocol
from log_message import LogMessage

@pytest.fixture
def log_message_with_header():
    return LogMessage("Test Header", "Test message", "Info", "example.py", 42)

def test_log_message_serialization_and_deserialization_with_header(log_message_with_header):
    # Serialize the log message to bytes
    log_bytes = log_message_with_header.to_bytes()

    # Deserialize the bytes back to a LogMessage instance
    new_log_message = LogMessage.from_bytes(log_bytes)

    # Assertions
    assert new_log_message.header == log_message_with_header.header
    assert new_log_message.message == log_message_with_header.message
    assert new_log_message.level == log_message_with_header.level
    assert new_log_message.file == log_message_with_header.file
    assert new_log_message.line == log_message_with_header.line

def test_always_fails(log_message_with_header):
    assert True
    print(f"message: {log_message_with_header.file}")

def test_log_message_header(log_message_with_header):
    # Assertions for the header
    assert log_message_with_header.header == "Test Header"

def test_change_header(log_message_with_header):
    # Change the header
    new_header = "New Test Header"
    log_message_with_header.header = new_header

    # Assertions for the changed header
    assert log_message_with_header.header == new_header

def test_log_message_display_with_new_header(capsys, log_message_with_header):
    # Set a new header and display the log message
    log_message_with_header.set_header("New Display Header")
    log_message_with_header.display()
    
    # Capture the output
    captured = capsys.readouterr()

    # Assertions for the displayed header in the captured output
    assert "New Display Header" in captured.out.strip()


def test_jrepp_header(log_message_with_header):
    object_bytes = pickle.dumps(log_message_with_header)
    message_bytes = protocol.create_message(log_message_with_header)
    assert message_bytes[0] == 0xd7
    assert int.from_bytes(message_bytes[1:2], 'little') == len(object_bytes)
    assert int.from_bytes(message_bytes[3:7], 'little') == zlib.crc32(object_bytes) 
    

def test_jrepp_decode(log_message_with_header):
    message = protocol.create_message(log_message_with_header)
    obj = protocol.decode_message(message)
    assert obj.message == "Test message"


