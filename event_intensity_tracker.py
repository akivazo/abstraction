from .event import event
from typing import Mapping
class events_intensity_tracker:
    def __init__(self) -> None:
        self.__event_map: Mapping[event, int] = {}

    def add_event(self, event: event, intensity: int):
        if event in self.__event_map:
            self.__event_map[event] += intensity
        else:
            self.__event_map[event] = intensity

    def get_event_intensity(self, event: event):
        return self.__event_map[event]