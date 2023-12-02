from enum import Enum
from typing import Optional

import uml_interpreter.model.diagrams.abstract as dg
import uml_interpreter.model.diagrams.class_diagram as cd


class SequenceDiagram(dg.BehavioralDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.actors: list[SequenceActor] = []


class SequenceActor:
    def __init__(self, name: str) -> None:
        self.messages_from: list[SequenceMessage] = []
        self.messages_to: list[SequenceMessage] = []
        self.events: list[LifespanEvent] = []
        self.name = name


class LifespanEvent:
    def __init__(self) -> None:
        self.predecessor: Optional[LifespanEvent] = None
        self.successor: Optional[LifespanEvent] = None
        self.time: int = 0


class SequenceMessageStatus(Enum):
    FAILED = 0
    SUCCEEDED = 1


class SequenceMessage(LifespanEvent):
    def __init__(self, sender: SequenceActor, receiver: SequenceActor) -> None:
        super().__init__()
        self.sender = sender
        sender.messages_from.append(self)
        self.receiver = receiver
        receiver.messages_to.append(self)
        self.related_method: Optional[cd.ClassDiagramMethod] = None
        self.status: SequenceMessageStatus = SequenceMessageStatus.SUCCEEDED
        self.display_text: Optional[str] = None


class SyncSequenceMessage(SequenceMessage):
    def __init__(self, sender: SequenceActor, receiver: SequenceActor) -> None:
        super().__init__(sender, receiver)
        self.response: Optional[AsyncSequenceMessage] = None


class AsyncSequenceMessage(SequenceMessage):
    def __init__(self, sender: SequenceActor, receiver: SequenceActor) -> None:
        super().__init__(sender, receiver)
        self.response: Optional[SyncSequenceMessage] = None


class SequenceFragment(SequenceDiagram, LifespanEvent):
    def __init__(self, parent: SequenceDiagram, name: str) -> None:
        super().__init__(name)
        self.actors = parent.actors


class LoopSequenceFragment(SequenceFragment):
    def __init__(self, parent: SequenceDiagram, name: str) -> None:
        super().__init__(parent, name)


class ConditionSequenceFragment(SequenceFragment):
    def __init__(self, parent: SequenceDiagram, name: str) -> None:
        super().__init__(parent, name)
