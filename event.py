from dataclasses import dataclass
from typing import *
from abc import abstractmethod, ABC


class event(ABC):
    '''
    override this class to create your custom event
    '''
        
    @abstractmethod
    def __hash__(self) -> int:
        pass

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, event):
            return self.__hash__() == __value.__hash__()
        return False

    @abstractmethod
    def similarity(self, other: "event"):
        """
        Return the similarity of 'self' to 'other' event.
        '1' mean the same and '0' mean compleatly diffrent.
        """

        pass
    


    


class fake_event(event):

    def __hash__(self) -> int:
        raise NotImplementedError()
    
    def __add__(self, other: event):
        return other

class seperator(fake_event):
    def get_intensity(self):
        '''
        Return the intensity of the events that happend before the seperator.
        '''
