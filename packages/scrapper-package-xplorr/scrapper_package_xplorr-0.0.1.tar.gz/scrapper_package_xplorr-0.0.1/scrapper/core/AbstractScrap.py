from abc import ABC, abstractmethod

class DataScrap(ABC): # Inherit from ABC(Abstract base class)
    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def output(self):
        pass

    @abstractmethod
    def run(self, url):
        pass