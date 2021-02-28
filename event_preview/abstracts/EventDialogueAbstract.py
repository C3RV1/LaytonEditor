from .EventCharacterAbstract import EventCharacterAbstract


class EventDialogueAbstract:
    def __init__(self):
        pass

    def start_dialogue(self, character: EventCharacterAbstract, chr_anim, text, voice):
        pass

    def end_dialogue(self):
        pass
