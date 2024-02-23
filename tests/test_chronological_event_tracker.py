from ..chronological_event_tracker import chronological_event_tracker
from ..event import event
from dataclasses import dataclass

@dataclass
class string_event(event):
    string: str

def test_chronological_event_tracker():
    cet = chronological_event_tracker()
    events_strings = [
        "hello world",
        "hello world",
        "hello world",
        "hello wrld",
        "helo world",
        "helo wrld",
        "ello wold",
    ]
    for event_string in events_strings:
        events = event_string.split(" ")
        hello = events[0]
        world = events[1]
        hello_event = string_event(hello)
        hello_event.set_internal_events(list(hello))
        cet.event_happend(hello_event)
        world_event = string_event(world)
        world_event.set_internal_events(list(world))
        cet.event_happend(world_event)
    next_event = cet.get_next_strongest_event(event("hello"))
    assert next_event.string == "world"