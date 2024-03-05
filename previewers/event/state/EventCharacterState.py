import dataclasses


@dataclasses.dataclass
class EventCharacterState:
    slot: int
    anim: str
    fade: int
    visible: bool
