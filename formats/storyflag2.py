from enum import IntEnum
from formats.filesystem import FileFormat
from formats.binary import BinaryReader, BinaryWriter


class StoryStepConditionTypes(IntEnum):
    NONE = 0
    STORY_FLAG = 1
    PUZZLE_SOLVED = 2


class StoryStepCondition:
    def __init__(self, condition_type: StoryStepConditionTypes = StoryStepConditionTypes.NONE,
                 value: int = 0):
        self.condition_type = condition_type
        self.value = value

    def __repr__(self):
        if self.condition_type == StoryStepConditionTypes.NONE:
            return f"StoryStepCondition<NONE>"
        elif self.condition_type == StoryStepConditionTypes.STORY_FLAG:
            return f"StoryStepCondition<story flag {self.value}>"
        elif self.condition_type == StoryStepConditionTypes.PUZZLE_SOLVED:
            return f"StoryStepCondition<puzzle solved {self.value}>"

    @classmethod
    def read_stream(cls, rdr: BinaryReader):
        condition_type = rdr.read_uint16()
        value = rdr.read_uint16()
        if not 0 <= condition_type <= 2:
            raise ValueError(f"StoryStepConditionType not recognised ({condition_type})")
        if condition_type == 0:
            return None
        return cls(StoryStepConditionTypes(condition_type), value)

    def write_stream(self, wtr: BinaryWriter):
        wtr.write_uint16(self.condition_type)
        wtr.write_uint16(self.value)


class StoryStepEntry:
    def __init__(self, step_id: int = 0, story_step_conditions: list[StoryStepCondition] = None):
        self.step_id = step_id
        if story_step_conditions is not None:
            self.conditions = story_step_conditions
        else:
            self.conditions = []

    def __repr__(self):
        return f"StoryStep<id={self.step_id}, conditions={self.conditions}>"

    @classmethod
    def read_stream(cls, rdr: BinaryReader):
        step_id = rdr.read_uint16()
        conditions = []
        for _ in range(8):
            condition = StoryStepCondition.read_stream(rdr)
            if condition is not None:
                conditions.append(condition)
        return cls(step_id, conditions)

    def write_stream(self, wtr: BinaryWriter):
        wtr.write_uint16(self.step_id)
        if len(self.conditions) > 8:
            raise ValueError("A story step cannot have more than 8 conditions.")
        for condition in self.conditions:
            condition: StoryStepCondition
            condition.write_stream(wtr)
        for _ in range(8 - len(self.conditions)):
            condition = StoryStepCondition()
            condition.write_stream(wtr)


class StoryFlag2(FileFormat, list):
    def read_stream(self, stream):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)
        self.clear()
        for _ in range(256):
            story_step = StoryStepEntry.read_stream(rdr)
            if story_step.step_id == 0:
                continue
            self.append(story_step)

    def write_stream(self, stream):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)
        if len(self) > 256:
            raise ValueError("StoryFlag2 cannot have more than 256 entries.")

        self.sort(key=lambda e: e.step_id)
        for entry in self:
            entry: StoryStepEntry
            entry.write_stream(wtr)
        for _ in range(256 - len(self)):
            entry = StoryStepEntry()
            entry.write_stream(wtr)
