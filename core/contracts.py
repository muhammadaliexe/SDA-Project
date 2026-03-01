from abc import ABC, abstractmethod

class DataReader(ABC):
    @abstractmethod
    def read_data(self, file_path):
        pass

class DataWriter(ABC):
    @abstractmethod
    def write_data(self, data, result, config):
        pass