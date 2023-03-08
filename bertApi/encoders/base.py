import abc 
# Abstract base class for encoder each encoder need to implement encode() method of this base class
class Encoder(metaclass=abc.ABCMeta):  # python 3
    @abc.abstractmethod
    def encode(self, sentence: str):
        """required method"""
        return
