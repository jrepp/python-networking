from abc import abstractmethod

def decode(packet_bytes):
    return "OBJECT"


class LogMessage:
    def __init__(self, **kwargs):
        self.message = kwargs.get('message')

class ProtocolLayer:
    def __init__(self, log_processor):
        self.processor = log_processor

    def handle_packet(self, packet_bytes):
        # decode packet into object
        log = decode(packet_bytes)
        self.processor.process(log)


class LogProcessor:
    @abstractmethod
    def process(self, log: LogMessage) -> bool:
        return False

class LogProcessorList(LogProcessor):
    def __init__(self):
        self.processors = list()

    def add_processor(self, p):
        self.processors.append(p)

    def process(self, log):
        """
        Call all processors and returns True if any processor returned True
        """
        results = list()
        for p in self.processors:
            results.append(p.process(log))
        return any(results)

class PrintLogProcessor(LogProcessor):
    def __init__(self):
            pass

    def process(self, log):
        print(f"{log}")
        return True

class FilteredLogProcessor(LogProcessor):
    def __init__(self, filter_str, sub_processor):
        self.filter_str = filter_str
        self.sub_processor = sub_processor

    def process(self, log):
        if log.message.find(self.filter_str) > -1:
            return self.sub_processor.process(log)
        return False


class TestLogProcesor(LogProcessor):
    def __init__(self):
        self.process_count = 0

    def process(self, log: LogMessage) -> bool:
        self.process_count += 1
        return True

def test_log_processor_list():
    processors = LogProcessorList()

    lm1 = LogMessage(message="blah")
    lm2 = LogMessage(message="hello")

    # Configuration
    tlp1 = TestLogProcesor()
    tlp2 = TestLogProcesor()
    processors.add_processor(tlp1)
    processors.add_processor(tlp2)

    # Processing
    processors.process(lm1)
    processors.process(lm2)

    assert tlp1.process_count == 2
    assert tlp2.process_count == 2


if __name__ == '__main__':
    test_log_processor_list()
