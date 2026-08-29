from collections import OrderedDict, deque
from dataclasses import dataclass
from threading import RLock
from uuid import UUID


MAX_TURNS = 6
MAX_ACTIVE_SESSIONS = 32


@dataclass(frozen=True)
class Message:
    role: str
    content: str


class ConversationStore:
    """Bounded, process-local history. One turn is one user/assistant pair."""

    def __init__(self) -> None:
        self._sessions: OrderedDict[UUID, deque[Message]] = OrderedDict()
        self._lock = RLock()

    def history(self, session_id: UUID) -> list[dict[str, str]]:
        with self._lock:
            messages = self._sessions.get(session_id)
            if messages is None:
                return []
            self._sessions.move_to_end(session_id)
            return [{"role": item.role, "content": item.content} for item in messages]

    def append_turn(self, session_id: UUID, user_text: str, assistant_text: str) -> int:
        with self._lock:
            messages = self._sessions.setdefault(session_id, deque(maxlen=MAX_TURNS * 2))
            self._sessions.move_to_end(session_id)
            messages.append(Message(role="user", content=user_text))
            messages.append(Message(role="assistant", content=assistant_text))
            while len(self._sessions) > MAX_ACTIVE_SESSIONS:
                self._sessions.popitem(last=False)
            return len(messages) // 2

    def clear(self, session_id: UUID) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)
