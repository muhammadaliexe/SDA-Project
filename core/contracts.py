from typing import Protocol

class DataReader(Protocol):
    def read_data(self, file_path):
        pass

class DataSink(Protocol):
    def write_data(self, data, config):
        pass