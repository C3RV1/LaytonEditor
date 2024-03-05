import dataclasses


@dataclasses.dataclass
class EventBGState:
    background: str
    fade: int
    tint: tuple
