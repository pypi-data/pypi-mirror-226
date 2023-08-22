import os
import sys
from abc import ABC, abstractmethod

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class OurQueue(ABC):

    @abstractmethod
    def push(self, item):
        """push to the queue"""
        pass

    @abstractmethod
    def get(self):
        """get from the queue (and delete)"""
        pass

    @abstractmethod
    def peek(self):
        """get the head of the queue (without deleting)"""
        pass
